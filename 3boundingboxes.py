import cv2
import numpy as np

# Load the video
video_path = "/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/29 jan/four videos/c0.mp4"  # Update with your video file
cap = cv2.VideoCapture(video_path)

# Define bounding box coordinates
top_box = (1320, 185, 1334, 199)  # Top light
middle_box = (1320, 202, 1334, 216)  # Middle (Yellow) light
bottom_box = (1320, 218, 1334, 232)  # Bottom light

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
    if middle_brightness > top_brightness and middle_brightness > bottom_brightness:
        if not yellow_detected:
            start_frame = frame_index  # Start of yellow light detection
            yellow_detected = True
    else:
        if yellow_detected:
            yellow_frames.append((start_frame, frame_index - 1))  # End of yellow light detection
            yellow_detected = False
            start_frame = None

    frame_index += 1

# If the yellow light is detected in the last frames and the video ends
if yellow_detected:
    yellow_frames.append((start_frame, frame_index - 1))

cap.release()

# Output frame ranges where yellow light is detected
print("Yellow light detected at frames:", yellow_frames)
