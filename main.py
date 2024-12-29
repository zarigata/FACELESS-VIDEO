from ollama_generator import OllamaGenerator
from tts_script import TTSConverter
from video_script import VideoCompiler

def create_reel():
    # Initialize components
    generator = OllamaGenerator()
    tts_converter = TTSConverter()
    video_compiler = VideoCompiler()
    
    # Generate topic
    topic = generator.generate_topic()
    print("Generated Topic:", topic)
    
    # Generate script
    script = generator.generate_script(topic)
    print("\nGenerated Script:\n", script)
    
    # Convert script to speech
    audio_path, audio_duration = tts_converter.text_to_speech(script)
    print(f"\nAudio generated: {audio_path}")
    print(f"Audio duration: {audio_duration:.2f} seconds")
    
    # Compile video
    video_path = video_compiler.compile_video(audio_path)
    print(f"\nReel video created: {video_path}")

def main():
    create_reel()

if __name__ == "__main__":
    main()
