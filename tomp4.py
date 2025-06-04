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
# input_ts = 'rawData/La_Villita_Rd_EB_Signal/10.0.0.219_20250508064142_20250508104536.ts'
input_ts = 'rawData/La_Villita_Rd_EB_Signal/10.0.0.219_20250508104541_20250508140240.ts'
output_mp4 = 'rawData/fourCams/c0_1.mp4'
convert_ts_to_clean_mp4(input_ts, output_mp4)
