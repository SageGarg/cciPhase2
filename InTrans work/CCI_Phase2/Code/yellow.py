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

        while frame_count < 10:
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
    
    # Create black frames for padding
    black_frame = np.zeros((height, width, layers), dtype=np.uint8)
    
    # Pad frames_list with black frames if necessary
    max_length = max(len(frames) for frames in frames_list)
    padded_frames_list = [frames + [black_frame] * (max_length - len(frames)) for frames in frames_list]

    # Separate the first three videos and the fourth video
    top_row_frames = padded_frames_list[:3]
    bottom_row_frames = padded_frames_list[3] if len(padded_frames_list) > 3 else [black_frame] * max_length

    # Stitch top row (three videos side-by-side)
    stitched_frames = []
    for frames in zip(*top_row_frames):
        stitched_frame = np.hstack(frames)
        stitched_frames.append(stitched_frame)

    # Stitch bottom row (single video, same width as top row)
    for frame in bottom_row_frames:
        stitched_frame = np.hstack([frame, black_frame, black_frame])  # Adjust to center the single video
        stitched_frames.append(stitched_frame)
    
    # Determine the final frame dimensions
    stitched_height = height * 2  # Two rows
    stitched_width = width * 3  # Three videos side-by-side
    
    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (stitched_width, stitched_height))
    
    for frame in stitched_frames:
        out.write(frame)
    
    out.release()

# Main process
videos_path = r'/home/marya/Desktop/Sageena/cciPhase2/Utah/07302024/S/theVideos'  # Update with your path
frames_output_folder = r'/home/marya/Desktop/Sageena/cciPhase2/Utah/07302024/S/frames'  # Update with your path
final_video_output_folder = r'/home/marya/Desktop/Sageena/cciPhase2/Utah/07302024/S/yellow/yellow17--21'  # Update with your path

# Step 1: Extract first 50 frames
extract_first_50_frames(videos_path, frames_output_folder)

# Step 2: Manually delete frames to sync (done manually by user)

# Get list of videos
videos = [f for f in os.listdir(videos_path) if f.endswith('.mp4')]

# Step 3: Input starting frame counts
starting_frames = get_starting_frames(videos)

# Step 4: Specify frame intervals and create video clips
    
yellow_frames = [(113510, 113550), (114700, 114740), (115900, 115940), (117090, 117130), (118300, 118340), (119500, 119540), (120700, 120740), (121900, 121940), (123100, 123140), (124300, 124340), (125500, 125540), (126700, 126740), (127890, 127930), (129100, 129140), (130300, 130340), (131500, 131540), (132910, 132950), (134990, 135030), (136300, 136340), (137500, 137540), (138700, 138740), (139900, 139940), (141320, 141360), (142500, 142540), (143590, 143630), (144680, 144720), (145890, 145930), (147080, 147120), (148270, 148310), (149570, 149610), (150690, 150730), (151900, 151940), (153100, 153140), (154530, 154570), (156600, 156640), (157900, 157940), (159100, 159140), (160310, 160350), (161510, 161550), (162890, 162930), (166560, 166600), (167910, 167950), (168990, 169030), (170060, 170100), (171150, 171190), (172230, 172270), (173280, 173320), (175800, 175840), (176810, 176850), (177830, 177870), (178800, 178840), (179910, 179950), (181040, 181080), (182210, 182250), (183380, 183420), (185600, 185640), (186580, 186620), (187630, 187670), (188800, 188840), (190050, 190090), (191020, 191060), (192490, 192530), (193790, 193830), (194920, 194960), (195970, 196010), (197080, 197120), (198160, 198200), (199520, 199560), (200680, 200720), (201590, 201630), (202620, 202660), (203860, 203900), (205090, 205130), (206470, 206510), (207780, 207820), (209200, 209240), (210360, 210400), (211330, 211370), (212590, 212630), (213720, 213760), (214700, 214740), (215730, 215770), (217040, 217080), (218370, 218410), (219590, 219630), (220790, 220830), (221880, 221920), (223190, 223230), (224450, 224490), (225530, 225570), (226570, 226610), (227620, 227660), (228610, 228650), (229780, 229820), (230690, 230730), (231720, 231760), (232970, 233010), (234140, 234180), (235040, 235080), (236270, 236310), (237420, 237460), (238330, 238370), (239420, 239460), (240420, 240460), (241400, 241440), (242410, 242450), (243470, 243510), (244560, 244600), (245740, 245780), (246930, 246970), (247910, 247950), (248960, 249000), (249980, 250020), (251040, 251080), (252110, 252150), (253450, 253490), (254620, 254660), (255530, 255570)]
for start, end in yellow_frames:
    frames_list = []
    i = 0
    for video_name, start_frame in starting_frames.items():
        
        start_frame_adj = max(start_frame + (start - 80), 0)  # 8 seconds before
        #print(start_frame_adj)
        end_frame_adj = start_frame + (end + 80)  # 8 seconds after
        video_path = os.path.join(videos_path, video_name)
        frames = create_video_clip(start_frame_adj, end_frame_adj, video_path)
        if frames:
            frames_list.append(frames)

    stitched_video_output = os.path.join(final_video_output_folder, f'stitched_clip_{start}_{end}.mp4')
    stitch_frames(frames_list, stitched_video_output)

print("All processes completed successfully.")
