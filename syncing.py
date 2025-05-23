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
    "c0.mp4": 7,
    "c1.mp4": 488257,
    "c2.mp4": 488257,
    "c3.mp4": 488257
}

videos_path = '3500_S_EB/videos/fourCams'
frames_output_folder = '3500_S_EB/videos/frames'
final_video_output_folder = '3500_S_EB/videos/clips2'

# start_frame_offsets = extract_50_frames_from_input(videos_path, frames_output_folder)
videos = sorted([f for f in os.listdir(videos_path) if f.endswith(('.mp4', '.ts'))])
# starting_frames = get_starting_frames(videos)

yellow_frames =    [(484, 531), (1797, 1844), (3015, 3062), (4082, 4129), (5423, 5470), (6469, 6516), (7843, 7890), (8968, 9015), (10231, 10278), (11330, 11377), (12550, 12597), (13693, 13740), (14915, 14963), (16073, 16120), (17305, 17352), (18633, 18680), (19832, 19879), (21061, 21108), (22258, 22306), (23485, 23532), (24614, 24661), (25836, 25883), (26949, 26996), (28102, 28149), (29392, 29440), (30638, 30654), (30656, 30685), (31857, 31904), (33081, 33092), (33094, 33122), (33124, 33129), (34205, 34208), (34210, 34216), (34218, 34218), (34220, 34226), (34228, 34228), (34230, 34236), (34238, 34238), (34240, 34244), (34246, 34246), (34248, 34248), (34250, 34252), (35437, 35438), (35445, 35447), (35455, 35455), (35457, 35457), (35465, 35467), (35475, 35475), (35477, 35477), (35483, 35483), (36636, 36636), (36638, 36638), (36640, 36640), (36642, 36642), (36646, 36646), (36648, 36648), (36650, 36652), (36658, 36660), (36662, 36662), (36664, 36664), (36666, 36666), (36668, 36668), (36670, 36670), (36672, 36672), (36676, 36676), (36678, 36678), (36680, 36680), (36684, 36684), (37656, 37656), (37666, 37666), (37668, 37668), (37674, 37674), (37676, 37676), (37678, 37678), (37682, 37682), (37684, 37684), (37686, 37686), (37688, 37688), (37694, 37694), (37696, 37696), (37698, 37698), (37700, 37700), (37702, 37702), (38980, 38980), (38982, 38982), (38990, 38990), (38992, 38992), (39002, 39002), (39008, 39008), (39010, 39010), (39012, 39012), (39018, 39018), (39020, 39020), (39022, 39022), (40094, 40094), (40096, 40096), (40098, 40098), (40100, 40100), (40104, 40104), (40106, 40106), (40108, 40108), (40110, 40110), (40116, 40116), (40118, 40118), (40124, 40124), (40126, 40126), (40128, 40128), (40136, 40136), (54561, 54561), (55753, 55753), (55759, 55763), (55765, 55765), (55769, 55769), (55771, 55771), (55777, 55777), (55779, 55779), (55781, 55781), (55783, 55783), (55787, 55787), (55791, 55791), (55799, 55799), (56994, 56994), (58260, 58260), (58270, 58270), (58272, 58272), (58276, 58276), (58278, 58278), (58280, 58280), (58282, 58282), (58284, 58284), (58288, 58288), (58290, 58290), (58292, 58292), (60699, 60699)]
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
    
    stitched_video_output = os.path.join(final_video_output_folder, f'3500S_EB_3_{start}_{end}.mp4')
    stitch_frames(frames_list, stitched_video_output)