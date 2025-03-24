import os
import subprocess

# Input and output folder paths
input_folder = "NB/videos/Jan 29/signalHead"
output_folder = "NB/videos/Jan 29/signalHeadReducedFPS"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Set the new FPS
new_fps = 10

# Process each video file in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.mp4', '.ts', '.avi', '.mov', '.mkv')):  # Check for video file extensions
        input_video_path = os.path.join(input_folder, filename)
        output_video_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_10fps.mp4")
        
        # Use ffmpeg to change FPS without dropping frames (fps resampling)
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_video_path,  # Input video
            '-filter:v', f'fps={new_fps}',  # Set the desired FPS
            '-c:v', 'libx264',  # Use the H.264 codec for encoding
            '-preset', 'fast',  # Choose a fast encoding preset
            '-crf', '18',  # Set quality level (lower is better, 18 is visually lossless)
            '-c:a', 'copy',  # Keep the original audio without re-encoding
            output_video_path  # Output video path
        ]
        
        # Run the command
        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Processed: {filename} -> {output_video_path}")

print("Batch video processing complete.")
