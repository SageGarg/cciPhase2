from datetime import datetime

# List of timestamp tuples
timestamps = [
   ('16:01:24', '16:01:28'),
    ('16:04:14', '16:04:18'),
    ('16:07:05', '16:07:09'),
    ('16:09:55', '16:09:59'),
    ('16:12:44', '16:12:48'),
    ('16:15:34', '16:15:38'),
    ('16:18:25', '16:18:29'),
    ('16:21:16', '16:21:20'),
    ('16:24:05', '16:24:09'),
    ('16:26:54', '16:26:58'),
    ('16:29:44', '16:29:48'),
    ('16:32:34', '16:32:38'),
    ('16:35:23', '16:35:27'),
    ('16:38:18', '16:38:22'),
    ('16:41:05', '16:41:09'),
    ('16:43:54', '16:43:58'),
    ('16:46:43', '16:46:47'),
    ('16:49:32', '16:49:36'),
    ('16:52:21', '16:52:25'),
    ('16:55:10', '16:55:14'),
    ('16:57:59', '16:58:03')
]

# Function to convert timestamp to frame number
def timestamp_to_frame(timestamp, fps=10):
    dt = datetime.strptime(timestamp, "%H:%M:%S")  # Changed from %I:%M:%S to %H:%M:%S
    total_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    return total_seconds * fps

# Convert timestamps to frames and create a list of tuples
frames = [(timestamp_to_frame(start), timestamp_to_frame(end)) for start, end in timestamps]

# Print the result
print(frames)
