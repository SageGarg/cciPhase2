import cv2
import numpy as np

# Load the video
video_path = "/home/sg1807/Desktop/sageena/cciPhase2/SLC/3500_S_EB/videos/fourCams/c0.mp4"
cap = cv2.VideoCapture(video_path)

# Define bounding box coordinates
top_box = (995, 364, 1013, 382)      # Top light (red)
middle_box = (995, 382, 1013, 400)   # Middle light (yellow)
bottom_box = (995, 400, 1013, 418)   # Bottom light (green)

# Parameters
BRIGHTNESS_MARGIN = 2  # Minimum difference to consider one light brighter
LOG_INTERVAL = 100     # Frames between brightness logs

# Output variables
yellow_frames = []
frame_index = 0
yellow_detected = False
start_frame = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print(f"Video read failed or ended at frame {frame_index}")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Extract boxes
    top_light = gray[top_box[1]:top_box[3], top_box[0]:top_box[2]]
    middle_light = gray[middle_box[1]:middle_box[3], middle_box[0]:middle_box[2]]
    bottom_light = gray[bottom_box[1]:bottom_box[3], bottom_box[0]:bottom_box[2]]

    # Compute mean brightness
    top_brightness = np.mean(top_light)
    middle_brightness = np.mean(middle_light)
    bottom_brightness = np.mean(bottom_light)

    # Debug logging
    if frame_index % LOG_INTERVAL == 0:
        print(f"Frame {frame_index}: Top={top_brightness:.1f}, Middle={middle_brightness:.1f}, Bottom={bottom_brightness:.1f}")

    # Detect yellow: middle box is noticeably brighter than top and bottom
    if (middle_brightness > top_brightness + BRIGHTNESS_MARGIN and
        middle_brightness > bottom_brightness + BRIGHTNESS_MARGIN):
        if not yellow_detected:
            start_frame = frame_index
            yellow_detected = True
    else:
        if yellow_detected:
            yellow_frames.append((start_frame, frame_index - 1))
            yellow_detected = False
            start_frame = None

    frame_index += 1

# Handle case where yellow light was on at end
if yellow_detected:
    yellow_frames.append((start_frame, frame_index - 1))

cap.release()

# Output result
print("\nYellow light detected at frame ranges:")
for start, end in yellow_frames:
    print(f"{start} to {end} (duration: {end - start + 1} frames)")
