import cv2

def count_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Total number of frames: {total_frames}")
    print(f"FPS: {fps}")
    
    cap.release()

# Replace with your .ts file path
video_file = "SLC/3500_S_EB/videos/fourCams/c0.mp4"
count_frames(video_file)
