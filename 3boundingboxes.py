import cv2
import numpy as np

# Load the video
video_path = "/home/sg1807/Desktop/sageena/cciPhase2/SLC/3500_S_EB/videos/fourCams/c0.mp4"  # Update with your video file
cap = cv2.VideoCapture(video_path)

# Define bounding box coordinates
top_box = (995, 364, 1013, 382)    # Top light (18x18 box, 36 pixels above bottom)
middle_box = (995, 382, 1013, 400)  # Middle (Yellow) light
bottom_box = (995, 400, 1013, 418)  # Bottom light
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

# Output frame ranges where yellow light is detected
print("Yellow light detected at frames:", yellow_frames)