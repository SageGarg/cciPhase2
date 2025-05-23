#!/bin/bash

# Check if user provided a file path
if [ -z "$1" ]; then
    echo "Usage: ./clean_one.sh /full/path/to/video.ts"
    exit 1
fi

input_file="$1"

# Ensure input file exists
if [ ! -f "$input_file" ]; then
    echo "❌ File not found: $input_file"
    exit 1
fi

# Extract directory and base name
input_dir=$(dirname "$input_file")
filename=$(basename "$input_file" .ts)
output_file="$input_dir/${filename}_cleaned.mp4"

# Clean and re-encode
echo "Cleaning $input_file..."
ffmpeg -err_detect ignore_err -i "$input_file" -c:v libx264 -preset fast -crf 23 -c:a copy "$output_file"

echo "✅ Cleaned video saved as: $output_file"
