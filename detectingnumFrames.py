import cv2
import os

# Path to the folder containing .ts video files
folder_path = 'SLC/3500_S_EB/videos/fourCams'

# List all files in the directory
video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

# Loop through each .ts file and get its FPS
for video_file in video_files:
    video_path = os.path.join(folder_path, video_file)
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error opening video file: {video_file}")
        continue
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video: {video_file}, FPS: {fps}")
    
    cap.release()
