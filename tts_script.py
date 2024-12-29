import os
import yaml
import torch
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

class TTSConverter:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.setup_tts()
    
    def setup_tts(self):
        """Initialize TTS model with voice reference"""
        model_manager = ModelManager()
        model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")
        
        reference_voice = self.config['paths']['reference_voice']
        
        # Use Tacotron2 for TTS
        self.tts_synthesizer = Synthesizer(
            model_path, 
            config_path,
            use_cuda=torch.cuda.is_available()
        )
        
        self.reference_voice = reference_voice
    
    def text_to_speech(self, text, output_path=None):
        """Convert text to speech and save as WAV"""
        if output_path is None:
            output_path = os.path.join(
                self.config['paths']['output'], 
                'reel_audio.wav'
            )
        
        # Generate speech using Tacotron2
        wav = self.tts_synthesizer.tts(text)
        
        self.tts_synthesizer.save_wav(wav, output_path)
        
        return output_path, len(wav) / self.tts_synthesizer.output_sample_rate
    
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
