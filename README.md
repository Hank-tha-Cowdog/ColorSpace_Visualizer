# ColorSpace_Visualizer
A Python-based GUI tool for analyzing and visualizing color spaces in video content. This application allows users to load video files and examine their color distribution in 3D space, with specific support for comparing against the Rec.709 color space standard.
Features

Load and analyze video files (supports .mp4, .avi, .mov)
3D visualization of color distribution
Comparison with Rec.709 color space boundaries
Detection and highlighting of out-of-gamut colors
Real-time toggling between different visualization options

Use Cases

Color grading verification for video content
Analyzing color space compliance with broadcast standards
Identifying out-of-gamut colors in video footage
Quality control for video production
Educational tool for understanding color spaces

Technical Details

Built with PyQt5 for the GUI
Uses OpenCV for video processing
Implements proper color space transformations via the colour library
Supports chromatic adaptation using Bradford transform
Includes white point handling for accurate color representation

Dependencies

PyQt5
OpenCV (cv2)
numpy
colour
matplotlib

Usage

Launch the application
Click "Load File" to select a video
Use the checkboxes to toggle between viewing Rec.709 boundaries and input color space
Click "Analyze" to process the video and view results
