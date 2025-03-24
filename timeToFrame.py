import sys


print("enter timestamps below:")
# Read timestamps directly from standard input
timestamps = [line.strip() for line in sys.stdin if line.strip()]

def time_to_frames(time_str, fps=10):
    h, m, s = map(int, time_str.split(':'))
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds * fps

# Compute frame numbers based on FPS
frame_tuples = [(time_to_frames(t), time_to_frames(t) + 40) for t in timestamps]

# Print the resulting list
print(frame_tuples)

