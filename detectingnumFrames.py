import cv2

# Path to your video file
video_path = '/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/29 jan/changedFrame/10.0.0.219_20250129014135_20250129082416_10fps.mp4'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video was opened successfully
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_POS_FRAMES)
print(f"Video: {video_path}, FPS: {fps}")


# Release the video capture object
cap.release()
