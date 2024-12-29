import os
import random
import yaml
import torch
import requests
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import moviepy.editor as mp
from pydub import AudioSegment
import ollama

class InstagramReelMaker:
    def __init__(self, config_path='config.yaml'):
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Setup Ollama connection
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Setup TTS
        self.setup_tts()
        
    def setup_tts(self):
        # Initialize Coqui TTS with voice cloning
        model_manager = ModelManager()
        model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")
        
        # Use reference voice for cloning
        reference_voice = 'j:/_____ PYTHON ______/FACELESS VIDEO/assets/voices/b2b88aee-0c56-4dc5-8462-608ec07a14d4.wav'
        
        self.tts_synthesizer = Synthesizer(
            model_path, 
            config_path,
            use_cuda=torch.cuda.is_available()
        )
        
        # Store reference voice path for potential future use
        self.reference_voice = reference_voice
    
    def generate_ai_content(self):
        # Generate content using Ollama
        response = ollama.generate(
            model=self.config['ollama']['model'], 
            prompt=self.config['ollama']['preprompt'],
            options={
                'temperature': self.config['ollama']['temperature'],
                'num_predict': self.config['ollama']['max_tokens']
            }
        )
        return response['response']
    
    def text_to_speech(self, text):
        # Convert text to speech
        wav = self.tts_synthesizer.tts(text)
        tts_path = 'temp_tts.wav'
        self.tts_synthesizer.save_wav(wav, tts_path)
        return tts_path
    
    def select_background_video(self):
        # Randomly select a background video
        backgrounds = os.listdir(self.config['paths']['backgrounds'])
        return os.path.join(self.config['paths']['backgrounds'], backgrounds[0])  # Always use first video
    
    def select_music(self):
        # Randomly select background music
        music_files = os.listdir(self.config['paths']['music'])
        return os.path.join(self.config['paths']['music'], music_files[0])  # Always use first music
    
    def combine_video_audio(self, video_path, tts_path, music_path):
        # Load video and audio clips
        video_clip = mp.VideoFileClip(video_path)
        tts_audio = AudioSegment.from_wav(tts_path)
        music_audio = AudioSegment.from_mp3(music_path)
        
        # Adjust audio lengths and volumes
        if len(tts_audio) > video_clip.duration * 1000:
            tts_audio = tts_audio[:int(video_clip.duration * 1000)]
        
        # Reduce music volume to 30% of voice volume
        music_audio = music_audio - 10  # Reduce by 10 dB (approximately 30% volume)
        
        # Combine audio with reduced music volume
        combined_audio = tts_audio.overlay(music_audio)
        combined_audio.export('temp_combined_audio.mp3', format='mp3')
        
        # Add audio to video
        audio_clip = mp.AudioFileClip('temp_combined_audio.mp3')
        final_clip = video_clip.set_audio(audio_clip)
        
        # Ensure video is full duration
        if final_clip.duration < self.config['video']['duration']:
            # Repeat video to fill duration
            final_clip = final_clip.loop(duration=self.config['video']['duration'])
        
        # Export final reel
        output_path = os.path.join(
            self.config['paths']['output'], 
            f'reel_{random.randint(1000, 9999)}.mp4'
        )
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # Close clips to release resources
        video_clip.close()
        audio_clip.close()
        final_clip.close()
        
        return output_path
    
    def create_reel(self):
        # Main reel creation workflow
        ai_content = self.generate_ai_content()
        tts_path = self.text_to_speech(ai_content)
        background_video = self.select_background_video()
        background_music = self.select_music()
        
        reel_path = self.combine_video_audio(background_video, tts_path, background_music)
        print(f"Reel created: {reel_path}")
        
        # Optional: cleanup temporary files
        os.remove(tts_path)
        os.remove('temp_combined_audio.mp3')
        
        return reel_path

def main():
    reel_maker = InstagramReelMaker()
    reel_maker.create_reel()

if __name__ == "__main__":
    main()
