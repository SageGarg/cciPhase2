import cv2
import numpy as np

# Load the video
video_path = "/home/sg1807/Desktop/sageena/cciPhase2/current/raw data/fourCams/c0.mp4"  # Update with your video file
cap = cv2.VideoCapture(video_path)


# Define bounding box coordinates (10x10 size)
top_box = (1140, 304, 1150, 314)     # Top light
middle_box = (1140, 314, 1150, 324)  # Middle (Yellow) light
bottom_box = (1140, 324, 1150, 334)  # Bottom light (top-left at 1140, 324)


BRIGHTNESS_MARGIN = 2  # You can adjust this if needed


yellow_frames = []
frame_index = 0
yellow_detected = False
start_frame = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Crop out the three boxes
    top_light = gray[top_box[1]:top_box[3], top_box[0]:top_box[2]]
    middle_light = gray[middle_box[1]:middle_box[3], middle_box[0]:middle_box[2]]
    bottom_light = gray[bottom_box[1]:bottom_box[3], bottom_box[0]:bottom_box[2]]

    # Compute brightness (mean pixel intensity)
    top_brightness = np.mean(top_light)
    middle_brightness = np.mean(middle_light)
    bottom_brightness = np.mean(bottom_light)

    # If the middle box is brighter than the others, it's likely yellow
    if (middle_brightness > top_brightness + BRIGHTNESS_MARGIN and middle_brightness > bottom_brightness + BRIGHTNESS_MARGIN):

        if not yellow_detected:
            start_frame = frame_index  # Start of yellow light detection
            yellow_detected = True
    else:
        if yellow_detected:
            yellow_frames.append((start_frame, frame_index - 1))  # End of yellow light detection
            yellow_detected = False
            # print(start_frame)
            start_frame = None
            # print(start_frame)

    frame_index += 1

# If the yellow light is detected in the last frames and the video ends
if yellow_detected:
    yellow_frames.append((start_frame, frame_index - 1))

cap.release()

# Merge nearby yellow frame ranges
merged_yellow_frames = []
GAP_THRESHOLD = 20  # Adjust how many frames apart is considered "close enough" to merge

for start, end in yellow_frames:
    if not merged_yellow_frames:
        merged_yellow_frames.append((start, end))
    else:
        prev_start, prev_end = merged_yellow_frames[-1]
        if start <= prev_end + GAP_THRESHOLD:
            # Extend the previous range
            merged_yellow_frames[-1] = (prev_start, max(prev_end, end))
        else:
            # Start a new range
            merged_yellow_frames.append((start, end))

# Output merged frame ranges
print("Merged yellow light frame ranges:", merged_yellow_frames)
print(">>>-----------------------------------------------")

# Output frame ranges where yellow light is detected
print("Yellow light detected at frames:", yellow_frames)