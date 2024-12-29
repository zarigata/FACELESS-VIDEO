import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

def combine_short_videos(directory, min_duration=60):
    """
    Combine short videos to meet a minimum total duration.
    
    :param directory: Path to directory containing videos
    :param min_duration: Minimum total video duration in seconds
    :return: Path to combined video
    """
    # List all video files
    video_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    
    # Shuffle videos for randomness
    random.shuffle(video_files)
    
    # Load video clips
    video_clips = []
    total_duration = 0
    
    for video_file in video_files:
        clip = VideoFileClip(os.path.join(directory, video_file))
        video_clips.append(clip)
        total_duration += clip.duration
        
        # Stop adding clips if we've reached minimum duration
        if total_duration >= min_duration:
            break
    
    # If not enough videos, repeat some
    while total_duration < min_duration:
        clip = random.choice(video_clips)
        video_clips.append(clip)
        total_duration += clip.duration
    
    # Concatenate videos
    final_clip = concatenate_videoclips(video_clips)
    
    # Trim to exact duration if needed
    if final_clip.duration > min_duration:
        final_clip = final_clip.subclip(0, min_duration)
    
    # Save combined video
    output_path = os.path.join(directory, f'combined_video_{random.randint(1000, 9999)}.mp4')
    final_clip.write_videofile(output_path, codec='libx264')
    
    return output_path

def main():
    backgrounds_dir = 'j:/_____ PYTHON ______/FACELESS VIDEO/assets/backgrounds'
    combined_video = combine_short_videos(backgrounds_dir)
    print(f"Combined video created: {combined_video}")

if __name__ == "__main__":
    main()
