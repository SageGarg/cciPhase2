import cv2
import os
import numpy as np

def extract_first_50_frames(videos_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    videos = os.listdir(videos_path)
    for video in videos:
        video_path = os.path.join(videos_path, video)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}.")
            continue

        frame_count = 0
        video_output_folder = os.path.join(output_folder, os.path.splitext(video)[0])
        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        while frame_count < 50:
            ret, frame = cap.read()
            if not ret:
                break

            frame_path = os.path.join(video_output_folder, f"frame_{frame_count + 1}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_count += 1

        cap.release()
        print(f"Extracted {frame_count} frames from {video}")

def get_starting_frames(videos):
    starting_frames = {}
    fm = []
    print("Enter the starting frame count for each video after synchronization:")
    for video in videos:
        start_frame = int(input(f"Starting frame for {video}: "))
        starting_frames[video] = start_frame
        fm.append(start_frame)

    return starting_frames

def create_video_clip(start_frame, end_frame, video_path, fps=10):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}.")
        return None

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_count = start_frame

    frames = []
    while frame_count <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        frame_count += 1

    cap.release()
    return frames

def stitch_frames(frames_list, output_file, fps=10):
    if not frames_list:
        print("No frames to stitch.")
        return
    
    # Determine the size of the frames
    height, width, layers = frames_list[0][0].shape
    stitched_width = width * len(frames_list)  # side-by-side
    
    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (stitched_width, height))
    
    # Pad frames_list with black frames if necessary
    black_frame = np.zeros((height, width, layers), dtype=np.uint8)
    max_length = max(len(frames) for frames in frames_list)
    padded_frames_list = [frames + [black_frame] * (max_length - len(frames)) for frames in frames_list]
    
    for frames in zip(*padded_frames_list):
        stitched_frame = np.hstack(frames)
        out.write(stitched_frame)
    
    out.release()

# Main process
videos_path = r'/home/marya/Desktop/Sageena/cciPhase2/Utah/07302024/S/theVideos'  # Update with your path
frames_output_folder = r'/home/marya/Desktop/Sageena/cciPhase2/Utah/07302024/S/frames'  # Update with your path
final_video_output_folder = r'/home/marya/Desktop/Sageena/cciPhase2/Utah/07302024/S/yellowSample'  # Update with your path

# Step 1: Extract first 50 frames
extract_first_50_frames(videos_path, frames_output_folder)

# Step 2: Manually delete frames to sync (done manually by user)

# Get list of videos and sort in reverse alphabetical order
videos = sorted([f for f in os.listdir(videos_path) if f.endswith('.mp4')], reverse=True)

# Step 3: Input starting frame counts
starting_frames = get_starting_frames(videos)

# Step 4: Specify frame intervals and create video clips
yellow_frames = [(265332, 265372), (266264, 266304), (267374, 267415), (268416, 268456), (269496, 269536), (270576, 270617), (271683, 271723), (272737, 272777), (273816, 273857), (274897, 274937), (276098, 276138), (276970, 277010), (278187, 278227), (279162, 279202), (280168, 280208), (281378, 281418), (282458, 282498), (283538, 283578), (284618, 284658), (285698, 285738), (286778, 286818), (287858, 287898), (288937, 288977), (290018, 290059), (291097, 291137), (292177, 292217), (293258, 293298), (294459, 294499), (295331, 295372), (296498, 296538), (297736, 297776), (298608, 298648), (299907, 299947)]

for start, end in yellow_frames:
    frames_list = []
    for video_name, start_frame in starting_frames.items():
        start_frame_adj = max(start_frame + (start - 80), 0)  # 8 seconds before
        end_frame_adj = start_frame + (end + 80)  # 8 seconds after
        video_path = os.path.join(videos_path, video_name)
        frames = create_video_clip(start_frame_adj, end_frame_adj, video_path)
        if frames:
            frames_list.append(frames)

    stitched_video_output = os.path.join(final_video_output_folder, f'stitched_clip_{start}_{end}.mp4')
    stitch_frames(frames_list, stitched_video_output)

print("All processes completed successfully.")
