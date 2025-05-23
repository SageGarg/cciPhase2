import subprocess

def convert_ts_to_clean_mp4(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264',        # Re-encode video to H.264 (very OpenCV-friendly)
        '-preset', 'fast',        # Reasonable speed
        '-crf', '22',             # Quality (lower = better, 18–28 range)
        '-c:a', 'aac',            # Re-encode audio
        '-movflags', '+faststart',  # Better for streaming/seeking
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Re-encoded video saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Re-encoding failed:", e)

# Usage:
input_ts = '3500_S_EB/videos/3500 S EB Signal - Line 21/10.0.0.219_20250410133344_20250410155526.ts'
output_mp4 = '3500_S_EB/videos/fourCams/c0_reencoded.mp4'
convert_ts_to_clean_mp4(input_ts, output_mp4)
