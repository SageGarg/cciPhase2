# The Yellow Light Project

## Overview

This project automates the detection of yellow light transitions and synchronizes multi-camera traffic videos for enhanced analysis and visualization. It forms part of a broader research effort focused on improving traffic safety and intersection efficiency through computer vision techniques.

## Problem Statement

Traffic signal timing is critical to road safety and traffic flow efficiency. Analyzing the precise onset of the yellow signal and corresponding driver behavior is essential for evaluating and optimizing traffic control measures.

## Data Description

- **Real-Time Videos**: Each dataset includes footage from **four cameras** at an intersection.
- **Signal Head Camera**: The closest camera, capturing the traffic signal directly, is provided in `.ts` format and records **4+ hours of video**.
- **Other Cameras**: Typically cover different angles and are used for synchronized analysis of traffic behavior.

## Methodology

### 1. Yellow Light Detection
Using the `.ts` video from the **signal head camera**, the system detects the **exact time frames where the yellow light is active**. This is achieved using OpenCV to monitor brightness changes within a predefined region of interest (ROI).

### 2. Synchronization
With the help of `syncing.py`, all four camera perspectives are **synchronized** based on timestamps. This ensures a coherent multi-angle view of each traffic event.

### 3. Clip Generation
Once yellow light onset is detected:
- A **20-second clip** is generated for each event:
  - **8 seconds before** yellow light
  - **4 seconds of yellow light**
  - **8 seconds after**

This provides a complete temporal context of vehicle behavior around the yellow transition.

## Purpose and Impact

This tool enables traffic engineers and researchers to:
- **Automatically detect yellow signal activation**
- **Synchronize footage from multiple traffic cameras**
- **Generate meaningful video clips** for further analysis and visualization

These capabilities are aimed at enhancing:
- **Intersection safety evaluation**
- **Traffic signal timing assessment**
- **Infrastructure planning and decision-making**

## Technologies Used

- Python
- OpenCV
- FFmpeg
- NumPy
- Pandas

## Repository Structure

