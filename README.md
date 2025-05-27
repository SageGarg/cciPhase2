# The Yellow Light Project

## Overview

This project automates the detection of yellow light transitions and synchronizes multi-camera traffic videos for enhanced analysis and visualization. It forms part of a broader research initiative aimed at improving traffic safety and intersection efficiency using computer vision.

## Problem Statement

Traffic signal timing is critical to road safety and traffic flow efficiency. Understanding the exact onset of the yellow light and analyzing driver responses during this interval is essential for evaluating and optimizing traffic control strategies.

## Data Description

- **Intersection Videos**: Each dataset includes footage from **four cameras** positioned at different angles around a traffic intersection.
- **Signal Head Camera**: A `.ts` format video capturing the traffic signal directly, typically over **4+ hours** of footage.
- **Other Cameras**: MP4 videos that cover alternative angles to observe vehicle behavior from multiple perspectives.

## Workflow and Methodology

### 1. Format Conversion (`tomp4.py`)

Converts the `.ts` file from the **signal head camera** to `.mp4`, making it compatible with OpenCV and other processing tools.

### 2. Yellow Light Detection (`3boundingboxes.py`)

Detects **yellow light onset** using brightness changes within predefined **bounding boxes**.

- Coordinates for these boxes can be determined using the first code snippet in `yellow_light_clip.ipynb`.
- Outputs the **exact frame numbers** corresponding to yellow light transitions.

### 3. Finding the Synced Frame (`fiftyFrames.py`)

- Extracts **50 frames** from each of the four camera videos.
- Helps visually identify the **perfectly synced frame number** across all videos.

### 4. Video Synchronization and Clip Generation (`syncing.py`)

Uses:
- **Yellow frame numbers** from `3boundingboxes.py`
- **Perfect sync frames** from `fiftyFrames.py`

Generates synchronized **20-second clips** for each yellow light event:
- **8 seconds before**
- **4–5 seconds during** yellow light
- **8 seconds after**

> ⚠️ **Note**: Before uploading or using any generated clip, verify that:
> - All four videos are **perfectly time-synced**
> - The **yellow light is clearly visible** in each clip

## Purpose and Impact

This tool allows traffic engineers and researchers to:
- **Automatically detect yellow signal activation**
- **Synchronize multi-camera traffic footage**
- **Generate meaningful, time-aligned video clips**

These capabilities support:
- **Intersection safety studies**
- **Traffic signal optimization**
- **Urban planning and infrastructure evaluation**

## Technologies Used

- Python  
- OpenCV  
- FFmpeg  
- NumPy  
- Pandas  

