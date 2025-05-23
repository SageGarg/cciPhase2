import cv2
import numpy as np

def time_to_seconds(t):
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

# Real-world start times
video_start_times = {
    "c0.mp4": time_to_seconds("13:31:03"),
    "c1.mp4": time_to_seconds("06:22:08"),
    "c2.mp4": time_to_seconds("06:03:09"),
    "c3.mp4": time_to_seconds("05:51:09")
}

# Sync window in real-world time (adjust as needed)
sync_start_time = time_to_seconds("15:35:00")  # 1:32 PM
sync_end_time = time_to_seconds("16:02:20")    # 1:32:20 PM
fps = 10
frame_width = 640
frame_height = 550

# Video order for final display: c3 | c2 | c1 | c0
video_order = ["/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/28 jan/3CAM/c3.mp4", "/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/28 jan/3CAM/c2.mp4", "/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/28 jan/3CAM/c1.mp4", "/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/28 jan/3CAM/c0.mp4"]

# Open video captures and calculate frame offsets
caps = []
start_frame = sync_start_time
end_frame = sync_end_time
frame_count = (end_frame - start_frame) * fps

for video in video_order:
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print(f"⚠️ Couldn't open {video}")
        continue

    import os
    real_start = video_start_times[os.path.basename(video)]

    offset = (sync_start_time - real_start) * fps

    # Skip to correct frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, offset)
    caps.append(cap)

# Setup output writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("synced_side_by_side.mp4", fourcc, fps, (frame_width * 4, frame_height))

# Read and write synchronized frames
for _ in range(int(frame_count)):
    frames = []
    for cap in caps:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ One of the videos ended early.")
            frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        else:
            frame = cv2.resize(frame, (frame_width, frame_height))
        frames.append(frame)

    combined = np.hstack(frames)
    out.write(combined)

# Cleanup
for cap in caps:
    cap.release()
out.release()
print("✅ Synced video saved as synced_side_by_side.mp4")
