import cv2
import os

def extract_50_frames(video_path, output_folder, start_frame):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    if start_frame >= total_frames:
        print("Error: Start frame exceeds video length.")
        return

    # Go to the start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    count = 1
    while count < 500:
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video or read error.")
            break
        filename = os.path.join(output_folder, f"frame_{count:03d}.jpg")
        cv2.imwrite(filename, frame)
        count += 1

    cap.release()
    print(f"Extracted {count} frames to '{output_folder}'.")

# === Change these paths if needed ===
video_file = "rawData/fourCams/c3.mp4"
start_frame = 268447
output_dir = "frames/testing"

extract_50_frames(video_file, output_dir, start_frame)
