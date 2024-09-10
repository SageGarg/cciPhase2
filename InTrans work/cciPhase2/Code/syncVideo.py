# import cv2
# import os

# # Function to synchronize and concatenate two videos side by side
# def synchronize_and_concatenate_videos(video1_path, video2_path, output_path):
#     cap1 = cv2.VideoCapture(video1_path)
#     cap2 = cv2.VideoCapture(video2_path)

#     # Get frame count and fps of the videos
#     frame_count = min(int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)))
#     fps = min(cap1.get(cv2.CAP_PROP_FPS), cap2.get(cv2.CAP_PROP_FPS))
#     width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Create VideoWriter object
#     out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width * 2, height))

#     # Read and write frames
#     for _ in range(frame_count):
#         ret1, frame1 = cap1.read()
#         ret2, frame2 = cap2.read()

#         if ret1 and ret2:
#             # Resize frames if needed to match height
#             if frame1.shape[0] != height:
#                 frame1 = cv2.resize(frame1, (int(width * height / frame1.shape[0]), height))
#             if frame2.shape[0] != height:
#                 frame2 = cv2.resize(frame2, (int(width * height / frame2.shape[0]), height))

#             # Concatenate frames side by side
#             concatenated_frame = cv2.hconcat([frame1, frame2])
#             out.write(concatenated_frame)

#     cap1.release()
#     cap2.release()
#     out.release()

# # Main function
# def main():
#     # Path to the two videos
#     video1_path = "001913_0063_20231114_000002.mp4"
#     video2_path = "200982_0042_20231114_000003.mp4"

#     # Output video path
#     output_path = "output_video.mp4"

#     # Synchronize and concatenate videos
#     synchronize_and_concatenate_videos(video1_path, video2_path, output_path)

#     print("Videos synchronized and concatenated successfully!")

# if __name__ == "__main__":
#     main()





# import cv2
# import os

# # Function to synchronize and concatenate a portion of two videos side by side
# def synchronize_and_concatenate_videos(video1_path, video2_path, output_path, start_time=12.0, end_time=12.5):
#     cap1 = cv2.VideoCapture(video1_path)
#     cap2 = cv2.VideoCapture(video2_path)

#     # Calculate start and end frames corresponding to the specified time range
#     fps = min(cap1.get(cv2.CAP_PROP_FPS), cap2.get(cv2.CAP_PROP_FPS))
#     start_frame = int(start_time * 3600 * fps)
#     end_frame = int(end_time * 3600 * fps)

#     # Get frame size
#     width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Create VideoWriter object
#     out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width * 2, height))

#     # Read and write frames
#     for frame_num in range(start_frame, end_frame):
#         cap1.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
#         cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

#         ret1, frame1 = cap1.read()
#         ret2, frame2 = cap2.read()

#         if ret1 and ret2:
#             # Resize frames if needed to match height
#             if frame1.shape[0] != height:
#                 frame1 = cv2.resize(frame1, (int(width * height / frame1.shape[0]), height))
#             if frame2.shape[0] != height:
#                 frame2 = cv2.resize(frame2, (int(width * height / frame2.shape[0]), height))

#             # Concatenate frames side by side
#             concatenated_frame = cv2.hconcat([frame1, frame2])
#             out.write(concatenated_frame)

#     cap1.release()
#     cap2.release()
#     out.release()

# # Main function
# def main():
#     # Path to the two videos
#     video1_path = "001913_0063_20231114_000002.mp4"
#     video2_path = "200982_0042_20231114_000003.mp4"

#     # Output video path
#     output_path = "output_video.mp4"

#     # Specify time range (in hours)
#     start_time = 12.0
#     end_time = 12.5

#     # Synchronize and concatenate videos for the specified time range
#     synchronize_and_concatenate_videos(video1_path, video2_path, output_path, start_time, end_time)

#     print("Videos synchronized and concatenated successfully!")

# if __name__ == "__main__":
#     main()

import cv2

# Function to synchronize and concatenate a portion of two videos side by side
def synchronize_and_concatenate_videos(ft81_path, ft182_path, ft320_path, output_path, start_time, end_time):
    cap1 = cv2.VideoCapture(ft81_path)
    cap2 = cv2.VideoCapture(ft182_path)
    cap3 = cv2.VideoCapture(ft320_path)

    # Calculate start and end frames corresponding to the specified time range
    fps = min(cap1.get(cv2.CAP_PROP_FPS), cap2.get(cv2.CAP_PROP_FPS), cap3.get(cv2.CAP_PROP_FPS))
    
    hours_1, minutes_1, seconds_1 = map(int, start_time.split(':'))

    total_seconds_1 = hours_1 * 3600 + minutes_1 * 60 + seconds_1   # Converting hh:mm:ss to total seconds

    start_frame_81ft = int(total_seconds_1 * fps) + 22
    start_frame_182ft = int(total_seconds_1 * fps) + 9
    start_frame_320ft = int(total_seconds_1 *fps)

    print('start_frame_81ft: ',start_frame_81ft)
    print('start_frame_182ft: ',start_frame_182ft)
    print('start_frame_320ft: ',start_frame_320ft)

    hours_2, minutes_2, seconds_2 = map(int, end_time.split(':'))

    total_seconds_2 = hours_2 * 3600 + minutes_2 * 60 + seconds_2
    end_frame = int(total_seconds_2 * fps)

    # Get frame size
    width = int(cap3.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap3.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create VideoWriter object
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width*3, height))

    # Read and write frames
    for frame_num in range(start_frame_320ft, end_frame):
        print('the frame num: ',frame_num, '/ 36000')
        cap3.set(cv2.CAP_PROP_POS_FRAMES, frame_num + start_frame_81ft - start_frame_320ft)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_num + start_frame_182ft - start_frame_320ft)
        cap1.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

        ret1, frame1 = cap3.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap1.read()

        if ret1 and ret2 and ret3:
            # Resize frames if needed to match height
            if frame3.shape[0] != height:
                frame3 = cv2.resize(frame3, (int(width * height / frame3.shape[0]), height))
            if frame2.shape[0] != height:
                frame2 = cv2.resize(frame2, (int(width * height / frame2.shape[0]), height))
            if frame1.shape[0] != height:
                frame1 = cv2.resize(frame1, (int(width * height / frame1.shape[0]), height))

            # Concatenate frames side by side
            concatenated_frame = cv2.hconcat([frame1, frame2, frame3])
            out.write(concatenated_frame)

    cap1.release()
    cap2.release()
    cap3.release()
    out.release()

# Main function
def main():
    # Path to the three videos
    ft81_path = r"//Users/sageena/InTrans work/cciPhase2/vishCode/the videos/Utah_Salt Lake_600 N_WB_81 ft from stop bar.mp4"
    ft182_path = r"/Users/sageena/InTrans work/cciPhase2/vishCode/the videos/Utah_Salt Lake_600 N_WB_182 ft from stop bar.mp4"
    ft320_path = r"/Users/sageena/InTrans work/cciPhase2/vishCode/the videos/Utah_Salt Lake_600 N_WB_320 ft from stop bar.mp4"

    # Output video path
    output_path = "ljl0-1_hr_output_of_3_videos.mp4"

    # Specify time range (in hours)
    start_time = "00:00:00"  # Start time in HH:MM:SS
    end_time = "0:59:59"    # End time in HH:MM:SS

    # Synchronize and concatenate videos for the specified time range
    synchronize_and_concatenate_videos(ft81_path, ft182_path, ft320_path, output_path, start_time, end_time)

    print("Videos synchronized and concatenated successfully!")

if __name__ == "__main__":
    main()
