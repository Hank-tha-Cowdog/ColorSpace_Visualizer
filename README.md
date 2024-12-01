# ColorSpace_Visualizer
![rgb_visualizer](https://github.com/user-attachments/assets/5fe3f3d1-ca99-4c4a-8717-566751839cac)


A Python-based GUI tool for analyzing and visualizing color spaces in video content. This application allows users to load video files and examine their color distribution in 3D space, with specific support for comparing against the Rec.709 color space standard.

## Features
- Load and analyze video files (supports .mp4, .avi, .mov)
- 3D visualization of color distribution
- Comparison with Rec.709 color space boundaries
- Detection and highlighting of out-of-gamut colors
- Real-time toggling between different visualization options

## Use Cases
- Color grading verification for video content
- Analyzing color space compliance with broadcast standards
- Identifying out-of-gamut colors in video footage
- Quality control for video production
- Educational tool for understanding color spaces

## Technical Details
- Built with PyQt5 for the GUI
- Uses OpenCV for video processing
- Implements proper color space transformations via the `colour` library
- Supports chromatic adaptation using Bradford transform
- Includes white point handling for accurate color representation

## Dependencies
- PyQt5
- OpenCV (cv2)
- numpy
- colour
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/color-space-analyzer.git
cd color-space-analyzer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install PyQt5 opencv-python numpy colour-science matplotlib
```

## Usage
1. Launch the application:
```bash
python color_space_analyzer.py
```
2. Click "Load File" to select a video
3. Use the checkboxes to toggle between viewing Rec.709 boundaries and input color space
4. Click "Analyze" to process the video and view results

## System Requirements
- Python 3.7 or higher
- At least 4GB RAM recommended for processing large video files
- Operating System: Windows, macOS, or Linux
