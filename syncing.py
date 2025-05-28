import cv2
import os
import numpy as np
    
def extract_50_frames_from_input(videos_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    videos = os.listdir(videos_path)
    start_frame_offsets = {}
    
    for video in videos:
        video_path = os.path.join(videos_path, video)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}.")
            continue
        
        start_frame_offset = int(input(f"Enter the starting frame for {video}: "))
        start_frame_offsets[video] = start_frame_offset
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_offset)
        
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
    
    return start_frame_offsets

def get_starting_frames(videos):
    starting_frames = {}
    print("Enter the starting frame count for each video after synchronization:")
    for video in videos:
        start_frame = int(input(f"Starting frame for {video}: "))
        starting_frames[video] = start_frame
    return starting_frames

def is_frame_black(frame, threshold=10):

    """Returns True if the frame is mostly black (low average pixel intensity)."""

    return np.mean(frame) < threshold
 


def create_video_clip(start_frame, end_frame, video_path, fps=10):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}.")
        return None

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_count = start_frame
    frames = []
    last_valid_frame = None
    total_frames_needed = end_frame - start_frame + 1

    while len(frames) < total_frames_needed:
        ret, frame = cap.read()

        if not ret:
            print(f"[WARN] Frame {frame_count} could not be read in {video_path}.")
            if last_valid_frame is not None:
                frames.append(last_valid_frame.copy())
            else:
                print(f"[ERROR] No valid frame available to use at frame {frame_count}. Filling with black.")
                black_frame = np.zeros((720, 1280, 3), dtype=np.uint8)  # fallback resolution
                frames.append(black_frame)
        else:
            if is_frame_black(frame) and last_valid_frame is not None:
                print(f"[WARN] Suspected black frame at {frame_count} in {video_path}, using previous frame.")
                frames.append(last_valid_frame.copy())
            else:
                frames.append(frame)
                last_valid_frame = frame

        frame_count += 1

    cap.release()
    return frames

 
 

def stitch_frames(frames_list, output_file, fps=10):
    if not frames_list:
        print("Error: No frames to stitch.")
        return
    
    max_height = max(frame.shape[0] for frames in frames_list for frame in frames)
    layers = frames_list[0][0].shape[2]

    # Resize frames to the maximum height while maintaining the aspect ratio
    def resize_frame(frame, target_height):
        h, w = frame.shape[:2]
        aspect_ratio = w / h
        new_width = int(target_height * aspect_ratio)
        return cv2.resize(frame, (new_width, target_height), interpolation=cv2.INTER_AREA)

    resized_frames_list = [
        [resize_frame(frame, max_height) for frame in frames]
        for frames in frames_list
    ]

    # Determine total stitched width
    stitched_width = sum(frames[0].shape[1] for frames in resized_frames_list)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (stitched_width, max_height))

    for frames in zip(*resized_frames_list):
        stitched_frame = np.hstack(frames)  # Horizontally concatenate frames
        out.write(stitched_frame)
    
    out.release()
    print(f"Stitched video saved to {output_file}")

anchor_frames = {
    "c0.mp4": 6,
    "c1.mp4": 268438,
    "c2.mp4": 268450,
    "c3.mp4": 268446
}

videos_path = 'rawData/fourCams'
frames_output_folder = 'frames'
final_video_output_folder = 'clips'

# start_frame_offsets = extract_50_frames_from_input(videos_path, frames_output_folder)
videos = sorted([f for f in os.listdir(videos_path) if f.endswith(('.mp4', '.ts'))])
# starting_frames = get_starting_frames(videos)

yellow_frames =    [(512, 561), (1764, 1813), (3552, 3601), (4974, 5023), (5843, 5892), (6893, 6942), (7570, 7619), (8320, 8369), (9429, 9478), (10405, 10454), (11626, 11675), (12692, 12741), (13587, 13636), (16140, 16189), (16950, 16999), (18350, 18399), (19269, 19318), (20361, 20410), (21193, 21242), (22319, 22368), (24540, 24589), (25558, 25607), (26821, 26870), (27375, 27424), (27906, 27955), (28784, 28833), (30293, 30342), (31104, 31153), (32005, 32054), (32557, 32606), (33630, 33679), (34763, 34811), (35945, 35994), (37105, 37154), (38209, 38258), (38610, 38658), (39226, 39274), (40027, 40076), (40746, 40795), (41812, 41861), (42684, 42733), (43751, 43800), (44594, 44643), (45828, 45877), (46728, 46777), (47311, 47360), (47699, 47748), (48649, 48698), (49228, 49277), (49858, 49907), (50473, 50522), (51159, 51208), (51815, 51864), (52401, 52450), (53487, 53536), (54705, 54754), (55988, 56037), (56889, 56937), (57264, 57312), (57937, 57986), (59000, 59049), (59734, 59783), (61741, 61790), (62085, 62134), (62749, 62798), (63490, 63539), (64411, 64460), (65244, 65293), (66828, 66877), (68898, 68946), (74254, 74303), (76763, 76812), (77754, 77803), (79830, 79879), (80322, 80371)]
# Example frame intervals

for idx, (start, end) in enumerate(yellow_frames):  # Iterate correctly over tuples
    frames_list = []
    for video_name in reversed(videos):
        relative_start = start - anchor_frames["c0.mp4"]
        relative_end = end - anchor_frames["c0.mp4"]

        actual_start = anchor_frames[video_name] + relative_start
        actual_end = anchor_frames[video_name] + relative_end

        # 8 seconds before and after
        start_frame_adj = actual_start - 80
        end_frame_adj = actual_end + 80


        video_path = os.path.join(videos_path, video_name)
        frames = create_video_clip(start_frame_adj, end_frame_adj, video_path)
        if frames:
            frames_list.append(frames)
    
    stitched_video_output = os.path.join(final_video_output_folder, f'3500S_EB_4_{start}_{end}.mp4')
    stitch_frames(frames_list, stitched_video_output)