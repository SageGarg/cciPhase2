import cv2
import os
import numpy as np

# Function to extract the first 50 frames from each video and save them to an output folder
def extract_first_50_frames(videos_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all videos in the provided path
    videos = os.listdir(videos_path)
    for video in videos:
        video_path = os.path.join(videos_path, video)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}.")
            continue

        frame_count = 0
        video_output_folder = os.path.join(output_folder, os.path.splitext(video)[0])
        # Create a folder for the current video's frames
        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        while frame_count < 50:
            ret, frame = cap.read()
            if not ret:
                break

            # Save each frame as a JPEG file
            frame_path = os.path.join(video_output_folder, f"frame_{frame_count + 1}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_count += 1

        cap.release()
        print(f"Extracted {frame_count} frames from {video}")

# Function to get the starting frame count for each video after synchronization
def get_starting_frames(videos):
    starting_frames = {}
    print("Enter the starting frame count for each video after synchronization:")
    for video in videos:
        # Prompt user for the starting frame count for each video
        start_frame = int(input(f"Starting frame for {video}: "))
        starting_frames[video] = start_frame

    return starting_frames

# Function to create a video clip from specified frame intervals
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

# Function to stitch multiple lists of frames into a single video output
# def stitch_frames(frames_list, output_file, fps=10):
#     if not frames_list:
#         print("No frames to stitch.")
#         return

#     # Determine the size of the frames
#     height, width, layers = frames_list[0][0].shape
#     stitched_width = width * len(frames_list)  # Combine frames side-by-side

#     # Create VideoWriter object
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_file, fourcc, fps, (stitched_width, height))

#     # Pad frames_list with black frames if necessary
#     black_frame = np.zeros((height, width, layers), dtype=np.uint8)
#     max_length = max(len(frames) for frames in frames_list)
#     padded_frames_list = [frames + [black_frame] * (max_length - len(frames)) for frames in frames_list]

#     for frames in zip(*padded_frames_list):
#         stitched_frame = np.hstack(frames)
#         out.write(stitched_frame)

#     out.release()

def stitch_frames(frames_list, output_file, fps=10):
    if len(frames_list) != 4:
        print("Error: Expected exactly 4 video inputs for 2x2 grid stitching.")
        return

    # Get frame dimensions
    height, width, layers = frames_list[0][0].shape
    black_frame = np.zeros((height, width, layers), dtype=np.uint8)

    # Pad frames_list with black frames if necessary
    max_length = max(len(frames) for frames in frames_list)
    padded_frames_list = [frames + [black_frame] * (max_length - len(frames)) for frames in frames_list]

    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width * 2, height * 2))

    for frames in zip(*padded_frames_list):
        # Arrange in 2x2 grid
        top_row = np.hstack((frames[0], frames[1]))  # Top: c1 (left), c2 (right)
        bottom_row = np.hstack((frames[2], frames[3]))  # Bottom: c3 (left), c4 (right)
        stitched_frame = np.vstack((top_row, bottom_row))  # Combine both rows

        out.write(stitched_frame)

    out.release()
    print(f"Stitched video saved to {output_file}")


videos_path = r'/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/29 jan/changedFrame'  # Update with your path
frames_output_folder = r'/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/frames/frame'  # Update with your path
final_video_output_folder = r'/home/sg1807/Desktop/sageena/cciPhase2/SLC/EB/videos/29 jan/processedClips2'  # Update with your path


# Step 1: Extract first 50 frames from each video
extract_first_50_frames(videos_path, frames_output_folder)

# Step 2: Manually delete frames to sync (User action required)

# Get list of videos from the directory
videos = sorted([f for f in os.listdir(videos_path) if f.endswith('.mp4')])


# Step 3: Input starting frame counts after synchronization
starting_frames = get_starting_frames(videos)

# Step 4: Specify frame intervals for clips and create video clips
yellow_frames =   [(883, 923), (3257, 3297), (5447, 5487), (7359, 7399), (9575, 9615), (12041, 12080), (14301, 14341), (16799, 16839), (18871, 18911), (20992, 21031), (23453, 23493), (25526, 25566), (27759, 27799), (28838, 28878), (31241, 31281), (33313, 33353), (35852, 35892), (38046, 38086), (39909, 39949), (42312, 42352), (44384, 44424), (46617, 46657), (49049, 49089), (51121, 51161), (53524, 53564), (54748, 54788), (57184, 57224), (58426, 58465), (60636, 60676), (63039, 63079), (65708, 65748), (67533, 67574), (68775, 68815), (71296, 71336), (73699, 73739), (75441, 75481), (77967, 78007), (80377, 80416), (82259, 82299)]
 # Define frame intervals here, one example has been provided.

for start, end in yellow_frames:
    frames_list = []
    for video_name, start_frame in starting_frames.items():
        # Adjust start and end frames for each video
        start_frame_adj = max(start_frame + (start - 80), 0)  # 8 seconds before
        end_frame_adj = start_frame + (end + 80)  # 8 seconds after

        video_path = os.path.join(videos_path, video_name)
        frames = create_video_clip(start_frame_adj, end_frame_adj, video_path)
        if frames:
            frames_list.append(frames)

    # Output the stitched video
    stitched_video_output = os.path.join(final_video_output_folder, f'MLK Jr Blvd NB @ SR 46__{start}_{end}.mp4')
    stitch_frames(frames_list, stitched_video_output)

print("All processes completed successfully.")
