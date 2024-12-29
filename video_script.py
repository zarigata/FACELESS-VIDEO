import os
import random
import yaml
import moviepy.editor as mp
from pydub import AudioSegment

class VideoCompiler:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def get_video_clips(self, audio_duration):
        """Select and prepare video clips to match audio duration"""
        backgrounds = os.listdir(self.config['paths']['backgrounds'])
        video_clips = []
        total_duration = 0
        
        # Shuffle backgrounds to ensure variety
        random.shuffle(backgrounds)
        
        while total_duration < audio_duration:
            for video_file in backgrounds:
                video_path = os.path.join(self.config['paths']['backgrounds'], video_file)
                clip = mp.VideoFileClip(video_path)
                
                # Ensure clip is not too short or too long
                clip_duration = min(clip.duration, max(2, audio_duration - total_duration))
                video_clips.append(clip.subclip(0, clip_duration))
                
                total_duration += clip_duration
                
                if total_duration >= audio_duration:
                    break
            
            # Prevent infinite loop and ensure we have enough content
            if len(video_clips) > 20 or total_duration >= audio_duration * 1.5:
                break
        
        return video_clips
    
    def compile_video(self, audio_path, output_path=None):
        """Compile video with background music and audio"""
        # Get audio duration
        audio = AudioSegment.from_wav(audio_path)
        audio_duration = len(audio) / 1000.0  # Convert to seconds
        
        # Select and prepare video clips
        video_clips = self.get_video_clips(audio_duration)
        
        # Ensure we have clips
        if not video_clips:
            raise ValueError("No video clips could be generated")
        
        final_video = mp.concatenate_videoclips(video_clips)
        
        # Add audio
        audio_clip = mp.AudioFileClip(audio_path)
        final_video = final_video.set_audio(audio_clip)
        
        # Add background music (optional)
        if self.config['video'].get('add_music', False):
            music_files = os.listdir(self.config['paths']['music'])
            music_path = os.path.join(self.config['paths']['music'], random.choice(music_files))
            music_clip = mp.AudioFileClip(music_path).subclip(0, audio_duration)
            
            # Reduce music volume
            music_volume_reduction = self.config['video'].get('music_volume_reduction', 10)
            music_clip = music_clip.volumex(0.2)  # Reduce to 20%
            
            # Overlay music with audio
            combined_audio = mp.CompositeAudioClip([audio_clip, music_clip])
            final_video = final_video.set_audio(combined_audio)
        
        # Set default output path
        if output_path is None:
            output_path = os.path.join(
                self.config['paths']['output'], 
                f'reel_{random.randint(1000, 9999)}.mp4'
            )
        
        # Write final video with better quality settings
        final_video.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac',
            preset='medium',  # Balance between quality and encoding speed
            fps=24  # Standard video frame rate
        )
        
        # Close clips to release resources
        for clip in video_clips + [final_video, audio_clip]:
            clip.close()
        
        return output_path

def main():
    compiler = VideoCompiler()
    audio_path = 'j:/_____ PYTHON ______/FACELESS VIDEO/output/reel_audio.wav'
    video_path = compiler.compile_video(audio_path)
    print(f"Reel video created: {video_path}")

if __name__ == "__main__":
    main()
