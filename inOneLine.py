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


videos_path = 'videos/29 jan/four videos'
frames_output_folder = 'frames/jan29'
final_video_output_folder = 'clips/jan29/signalHead5/new'

start_frame_offsets = extract_50_frames_from_input(videos_path, frames_output_folder)
videos = sorted([f for f in os.listdir(videos_path) if f.endswith('.mp4')])
starting_frames = get_starting_frames(videos)

yellow_frames =  [(560, 601), (1647, 1686), (2847, 2887), (4047, 4087), (5247, 5287), (6447, 6487), (7668, 7708), (8847, 8887), (10047, 10087), (11247, 11287), (12448, 12489), (13650, 13689), (14847, 14887), (16048, 16087), (17248, 17288), (18448, 18488), (19694, 19734), (20920, 20960), (22089, 22129), (23248, 23288), (24698, 24738), (26135, 26175), (26725, 26739), (27246, 27286), (28358, 28398), (29376, 29416), (30523, 30563), (31640, 31680), (32840, 32880), (34069, 34109), (35240, 35281), (36441, 36481), (37641, 37682), (38841, 38882), (40287, 40327), (41409, 41449), (42545, 42585), (43944, 43984), (45090, 45130), (46728, 46768), (47836, 47876), (48959, 48999), (50094, 50134), (51484, 51524), (52597, 52637), (53717, 53757), (54757, 54797), (55855, 55895), (56909, 56949), (58017, 58057), (59217, 59256), (60416, 60456), (61786, 61826), (62815, 62856), (64016, 64055), (65385, 65385), (65416, 65424), (66591, 66625), (67615, 67640), (68991, 69024), (70015, 70019), (70021, 70037), (70041, 70055), (71215, 71255), (72416, 72428), (72432, 72455), (73632, 73644), (74816, 74840), (76054, 76065), (76091, 76094), (77117, 77140), (77157, 77157), (78143, 78145), (78147, 78153), (78156, 78159), (78161, 78162), (78164, 78165), (78181, 78188), (79178, 79178), (80222, 80261), (81234, 81237), (81250, 81251), (81266, 81270), (82255, 82256), (83360, 83364), (84661, 84664), (84689, 84689), (84691, 84700), (85641, 85650), (85652, 85655), (85672, 85712), (86702, 86742), (87774, 87817), (88933, 88952), (89952, 89957), (90971, 91011), (92002, 92038), (92958, 92983), (93020, 93020), (94229, 94229), (94233, 94259), (95251, 95292), (96190, 96192), (96208, 96219), (96229, 96230), (97280, 97282), (97292, 97301), (97303, 97303), (97308, 97319), (97771, 97773), (97820, 97824), (97826, 97826), (98560, 98590), (99570, 99610), (100597, 100632), (100634, 100634), (100636, 100636), (101553, 101558), (101560, 101565), (101568, 101582), (101593, 101595), (103563, 103603), (104774, 104782), (105723, 105732), (105752, 105752), (105757, 105757), (106063, 106063), (106065, 106069), (106933, 106972), (108139, 108142), (108153, 108171), (108175, 108175), (108208, 108208), (109185, 109224), (110148, 110148), (111167, 111169), (111171, 111208), (111632, 111632), (112332, 112357), (112374, 112375), (112608, 112627), (113282, 113282), (113287, 113307), (113461, 113469), (113471, 113507), (114493, 114507), (114534, 114547), (114826, 114827), (114829, 114830), (114832, 114832), (115583, 115607), (116774, 116782), (117826, 117832), (118878, 118878), (118882, 118885), (118887, 118895), (118899, 118918), (120873, 120892), (120894, 120905), (120907, 120907), (120915, 120916)]
# Example frame intervals

for idx, (start, end) in enumerate(yellow_frames):  # Iterate correctly over tuples
    frames_list = []
    for video_name in reversed(videos):
        base_start_frame =  start_frame_offsets[video_name] + starting_frames[video_name] + start  # Use current tuple's start
        start_frame_adj = base_start_frame - 120  # 8 seconds before
        end_frame_adj = base_start_frame + 40 + 60  # 8 seconds after

        video_path = os.path.join(videos_path, video_name)
        frames = create_video_clip(start_frame_adj, end_frame_adj, video_path)
        if frames:
            frames_list.append(frames)
    
    stitched_video_output = os.path.join(final_video_output_folder, f'SLC_EB_Jan-29_signalHead5_{start}_{end}.mp4')
    stitch_frames(frames_list, stitched_video_output)

