import cv2
import os

# Input and output folder paths
input_folder = "videos/29 jan/001 012925 400 S Signal Heads - Line 79"
output_folder = "videos/29 jan/changedFrame"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Set the new FPS
new_fps = 10

# Process each video file in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.mp4', '.ts', '.avi', '.mov', '.mkv')):  # Check for video file extensions
        input_video_path = os.path.join(input_folder, filename)
        output_video_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_10fps.mp4")
        
        # Open the video file
        cap = cv2.VideoCapture(input_video_path)
        
        # Get the original properties of the video
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        original_fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        if original_fps == 0:
            print(f"Skipping {filename} due to FPS detection issue.")
            cap.release()
            continue
        
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, new_fps, (frame_width, frame_height))
        
        # Process frames: Keep only frames needed for 10 FPS
        frame_interval = max(1, original_fps // new_fps)  # Avoid division by zero
        frame_index = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Write every nth frame
            if frame_index % frame_interval == 0:
                out.write(frame)
            
            frame_index += 1
        
        # Release resources
        cap.release()
        out.release()
        print(f"Processed: {filename} -> {output_video_path}")

print("Batch video processing complete.")
