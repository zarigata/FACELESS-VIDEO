import os
import yaml
import torch
from TTS.api import TTS
from pydub import AudioSegment

class TTSConverter:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Determine device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize YourTTS for advanced voice cloning
        self.tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/your_tts", 
            progress_bar=False
        ).to(self.device)
        
        # Reference voice for cloning
        self.reference_voice = self.config['paths']['reference_voice']
    
    def text_to_speech(self, text, output_path=None, volume_boost=1.3):
        """
        Convert text to speech with voice cloning and volume boost
        
        Args:
            text (str): Text to convert to speech
            output_path (str, optional): Path to save audio
            volume_boost (float, optional): Multiplier to increase volume. Default is 30% boost.
        """
        if output_path is None:
            output_path = os.path.join(
                self.config['paths']['output'], 
                'reel_audio.wav'
            )
        
        # Generate speech using YourTTS with voice cloning
        self.tts.tts_to_file(
            text=text, 
            speaker_wav=self.reference_voice, 
            language="en", 
            file_path=output_path
        )
        
        # Optional: Boost volume using pydub
        audio = AudioSegment.from_wav(output_path)
        boosted_audio = audio + (volume_boost - 1) * 6  # Adjust volume in decibels
        boosted_audio.export(output_path, format="wav")
        
        return output_path, len(audio) / 1000  # Duration in seconds
    
def main():
    tts = TTSConverter()
    script = """
    Did you know the fascinating world of quantum physics challenges everything we understand about reality? 
    Imagine particles that can exist in multiple places simultaneously, or communicate instantaneously across vast distances. 
    Quantum mechanics reveals a universe far stranger and more mysterious than our everyday experience suggests.
    """
    audio_path, duration = tts.text_to_speech(script)
    print(f"Audio saved to {audio_path}")
    print(f"Audio duration: {duration:.2f} seconds")

if __name__ == "__main__":
    main()
