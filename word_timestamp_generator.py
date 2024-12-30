import os
import whisper
import cv2
import numpy as np
from moviepy.editor import VideoFileClip

class WordTimestampGenerator:
    def __init__(self, model_size='base'):
        """
        Initialize Whisper model for speech recognition
        
        :param model_size: Size of the Whisper model (tiny, base, small, medium, large)
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
    
    def generate_word_timestamps(self, audio_path):
        """
        Generate precise word timestamps from audio
        
        :param audio_path: Path to the audio file
        :return: List of word dictionaries with start, end times, and text
        """
        print("Transcribing audio with word-level timestamps...")
        result = self.model.transcribe(
            audio_path, 
            word_timestamps=True,
            # Adjust these parameters for more precise results
            condition_on_previous_text=False,
            verbose=False
        )
        
        # Extract word-level information
        word_timestamps = []
        for segment in result.get('segments', []):
            for word_info in segment.get('words', []):
                word_timestamps.append({
                    'text': word_info['word'].strip(),
                    'start': word_info['start'],
                    'end': word_info['end']
                })
        
        return word_timestamps
    
    def save_word_timestamps(self, word_timestamps, output_path):
        """
        Save word timestamps to a text file
        
        :param word_timestamps: List of word timestamp dictionaries
        :param output_path: Path to save the timestamps
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for word_data in word_timestamps:
                # Ensure text doesn't contain commas to prevent parsing issues
                safe_text = word_data['text'].replace(',', ' ')
                f.write(f"{word_data['start']:.2f},{word_data['end']:.2f},{safe_text}\n")
        
        print(f"Word timestamps saved to {output_path}")
    
    def render_subtitles(self, video_path, word_timestamps_path, output_path):
        """
        Render subtitles on video based on word timestamps
        
        :param video_path: Path to input video
        :param word_timestamps_path: Path to word timestamps file
        :param output_path: Path to output video with subtitles
        """
        # Read word timestamps
        word_timestamps = []
        with open(word_timestamps_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Split only the first two commas
                parts = line.strip().split(',', 2)
                start = float(parts[0])
                end = float(parts[1])
                text = parts[2]
                word_timestamps.append({
                    'start': start,
                    'end': end,
                    'text': text
                })
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            current_time = frame_count / fps
            
            # Find current words
            current_words = [
                word for word in word_timestamps 
                if word['start'] <= current_time <= word['end']
            ]
            
            if current_words:
                # Create subtitle text
                subtitle_text = ' '.join(word['text'] for word in current_words)
                
                # Text rendering parameters
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
            if frame_count % 30 == 0:
                progress = (frame_count / cap.get(cv2.CAP_PROP_FRAME_COUNT)) * 100
                print(f"\rProcessing: {progress:.1f}%", end="")
        
        # Clean up
        cap.release()
        out.release()
        
        # Copy audio from original video
        original_video = VideoFileClip(video_path)
        subtitled_video = VideoFileClip(output_path)
        final_video = subtitled_video.set_audio(original_video.audio)
        
        # Save final video
        final_video_path = output_path.replace('.mp4', '_with_audio.mp4')
        final_video.write_videofile(final_video_path)
        
        # Clean up
        original_video.close()
        subtitled_video.close()
        final_video.close()
        
        return final_video_path

def process_latest_video():
    """
    Process the most recent video in the output directory
    """
    output_dir = "j:/_____ PYTHON ______/FACELESS VIDEO/output"
    
    # Print directory contents for debugging
    print("Contents of output directory:")
    for item in os.listdir(output_dir):
        print(item)
    
    videos = [f for f in os.listdir(output_dir) if f.endswith('.mp4') and not f.endswith('_subtitled.mp4')]
    
    if not videos:
        print("No videos found to process.")
        return
    
    # Get the most recent video
    latest_video = max([os.path.join(output_dir, v) for v in videos], key=os.path.getctime)
    
    # Hardcode the audio path for now
    audio_path = os.path.join(output_dir, 'reel_audio.wav')
    
    if not os.path.exists(audio_path):
        print(f"No audio file found at {audio_path}")
        return
    
    # Timestamp output path
    timestamps_path = latest_video.replace('.mp4', '_word_timestamps.txt')
    
    # Subtitled video output path
    subtitled_video_path = latest_video.replace('.mp4', '_ai_subtitled.mp4')
    
    # Generate word timestamps
    generator = WordTimestampGenerator()
    word_timestamps = generator.generate_word_timestamps(audio_path)
    
    # Save word timestamps
    generator.save_word_timestamps(word_timestamps, timestamps_path)
    
    # Render subtitles
    final_video_path = generator.render_subtitles(
        latest_video, 
        timestamps_path, 
        subtitled_video_path
    )
    
    print(f"Created AI-subtitled video: {final_video_path}")

if __name__ == "__main__":
    process_latest_video()
