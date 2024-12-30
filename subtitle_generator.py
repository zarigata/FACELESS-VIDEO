import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip

class SubtitleGenerator:
    def __init__(self, script_path):
        self.script_path = script_path
    
    def read_script(self):
        with open(self.script_path, 'r') as f:
            return f.read()
    
    def generate_word_timings(self, video_duration):
        """Generate word timings from the script"""
        script_text = self.read_script()
        words = script_text.split()
        
        # Distribute words evenly across video duration
        word_duration = video_duration / len(words)
        
        word_timings = []
        for i, word in enumerate(words):
            start_time = i * word_duration
            end_time = start_time + word_duration
            word_timings.append((word, start_time, end_time))
        
        return word_timings

    def create_subtitles(self, output_path):
        """Create subtitle file and overlay on video"""
        try:
            # Load video
            cap = cv2.VideoCapture(output_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Calculate video duration
            video_duration = total_frames / fps
            
            # Generate word timings
            word_timings = self.generate_word_timings(video_duration)
            
            # Create output video writer
            subtitle_video_path = output_path.replace('.mp4', '_subtitled.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(subtitle_video_path, fourcc, fps, (width, height))
            
            # Process each frame
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = frame_count / fps
                
                # Find current word
                current_words = []
                for word, start, end in word_timings:
                    if start <= current_time <= end:
                        current_words.append(word)
                
                if current_words:
                    # Create subtitle text
                    subtitle_text = ' '.join(current_words)
                    
                    # Get text size
                    font = cv2.FONT_HERSHEY_DUPLEX
                    font_scale = height / 720  # Scale font based on video height
                    thickness = max(2, int(font_scale * 2))
                    
                    # Calculate text size and position
                    (text_width, text_height), baseline = cv2.getTextSize(
                        subtitle_text, font, font_scale, thickness
                    )
                    text_x = (width - text_width) // 2
                    text_y = height - 50  # 50 pixels from bottom
                    
                    # Draw text outline (black)
                    for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                        cv2.putText(
                            frame, subtitle_text,
                            (text_x + dx, text_y + dy),
                            font, font_scale, (0,0,0), thickness + 1,
                            cv2.LINE_AA
                        )
                    
                    # Draw text (white)
                    cv2.putText(
                        frame, subtitle_text,
                        (text_x, text_y),
                        font, font_scale, (255,255,255), thickness,
                        cv2.LINE_AA
                    )
                
                out.write(frame)
                frame_count += 1
                
                # Print progress
                if frame_count % 30 == 0:  # Update every 30 frames
                    progress = (frame_count / total_frames) * 100
                    print(f"\rProcessing: {progress:.1f}%", end="")
            
            print("\nFinished processing frames")
            
            # Release video objects
            cap.release()
            out.release()
            
            # Copy audio from original to new video
            print("Copying audio...")
            original = VideoFileClip(output_path)
            new_video = VideoFileClip(subtitle_video_path)
            final_video = new_video.set_audio(original.audio)
            
            # Save final video with audio
            final_video_path = subtitle_video_path.replace('.mp4', '_with_audio.mp4')
            final_video.write_videofile(final_video_path)
            
            # Clean up
            original.close()
            new_video.close()
            final_video.close()
            
            # Replace the non-audio version with the audio version
            os.remove(subtitle_video_path)
            os.rename(final_video_path, subtitle_video_path)
            
            return subtitle_video_path
            
        except Exception as e:
            print(f"Error creating subtitles: {e}")
            import traceback
            traceback.print_exc()
            return output_path

def add_subtitles_to_last_video():
    """Find the most recent video and add subtitles"""
    output_dir = "j:/_____ PYTHON ______/FACELESS VIDEO/output"
    videos = [f for f in os.listdir(output_dir) if f.endswith('.mp4') and not f.endswith('_subtitled.mp4')]
    
    if not videos:
        print("No videos found to add subtitles to.")
        return
    
    # Get the most recent video
    latest_video = max([os.path.join(output_dir, v) for v in videos], key=os.path.getctime)
    
    # Find or create the corresponding script
    script_path = latest_video.replace('.mp4', '.txt')
    
    if not os.path.exists(script_path):
        # Create a default script based on the filename
        default_script = f"This is a video about {os.path.splitext(os.path.basename(latest_video))[0]}"
        with open(script_path, 'w') as f:
            f.write(default_script)
        print(f"Created default script for {latest_video}")
    
    # Create subtitle generator
    subtitle_gen = SubtitleGenerator(script_path)
    
    # Add subtitles
    subtitled_path = subtitle_gen.create_subtitles(latest_video)
    print(f"Created subtitled video: {subtitled_path}")

if __name__ == "__main__":
    add_subtitles_to_last_video()
