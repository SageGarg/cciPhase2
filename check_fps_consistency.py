import subprocess
import sys
import os

def extract_timestamps(video_path):
    cmd = [
        "ffprobe",
        "-select_streams", "v",
        "-show_entries", "frame=best_effort_timestamp_time",
        "-of", "csv=p=0",
        "-v", "quiet",
        video_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        timestamps = [float(line.strip()) for line in lines if line.strip()]
        return timestamps
    except subprocess.CalledProcessError as e:
        print("Error running ffprobe:", e.stderr)
        return None

def check_fps_consistency(timestamps, expected_interval=0.1, tolerance=0.005):
    deltas = [round(timestamps[i+1] - timestamps[i], 6) for i in range(len(timestamps)-1)]
    irregular = [(i, d) for i, d in enumerate(deltas) if abs(d - expected_interval) > tolerance]
    return deltas, irregular

def main(video_path):
    if not os.path.isfile(video_path):
        print(f"Error: File not found - {video_path}")
        return

    print(f"Analyzing video: {video_path}")
    timestamps = extract_timestamps(video_path)
    if not timestamps:
        print("Failed to extract timestamps.")
        return

    deltas, irregular = check_fps_consistency(timestamps)

    print(f"Total frames: {len(timestamps)}")
    print(f"Expected interval: 0.1s (10 FPS)")
    print(f"Detected irregular frames: {len(irregular)}")

    if irregular:
        print("\nSample irregularities (frame index, interval):")
        for idx, (i, d) in enumerate(irregular[:10]):
            print(f"  Frame {i} ➝ {i+1}: Interval = {d:.6f} sec")
        print("\n⚠️ FPS is NOT consistent. Consider re-encoding.")
    else:
        print("✅ FPS is consistent at 10 FPS.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_fps_consistency.py path_to_video")
    else:
        main(sys.argv[1])
