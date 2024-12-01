# ColorSpace_Visualizer
import cv2
import numpy as np
import colour
from PyQt5 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys

class ColorSpaceAnalyzer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ColorSpace Analyzer')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        self.loadButton = QtWidgets.QPushButton('Load File')
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)

        self.analyzeButton = QtWidgets.QPushButton('Analyze')
        self.analyzeButton.setStyleSheet('QPushButton { background-color: green; }')
        self.analyzeButton.clicked.connect(self.analyzeColorSpace)
        layout.addWidget(self.analyzeButton)

        self.rec709CheckBox = QtWidgets.QCheckBox('Show REC709 Color Space')
        self.rec709CheckBox.setChecked(True)
        self.rec709CheckBox.stateChanged.connect(self.updatePlot)
        layout.addWidget(self.rec709CheckBox)

        self.inputColorCheckBox = QtWidgets.QCheckBox('Show Input Color Space')
        self.inputColorCheckBox.setEnabled(False)
        self.inputColorCheckBox.stateChanged.connect(self.updatePlot)
        layout.addWidget(self.inputColorCheckBox)

        self.infoLabel = QtWidgets.QLabel('No file loaded')
        layout.addWidget(self.infoLabel)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.filePath = None

    def loadFile(self):
        options = QtWidgets.QFileDialog.Options()
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Video File", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if self.filePath:
            self.infoLabel.setText(f'Loaded file: {self.filePath}')
            self.inputColorCheckBox.setEnabled(True)

    def sample_video_frames(self, video_path, num_samples=10):
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sampled_frames = []
        step = max(1, frame_count // num_samples)

        for i in range(0, frame_count, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                sampled_frames.append(frame)
            if len(sampled_frames) >= num_samples:
                break

        cap.release()
        return sampled_frames

    def analyzeColorSpace(self):
        if not self.filePath:
            return
        
        sampled_frames = self.sample_video_frames(self.filePath)
        all_pixels = []

        for frame in sampled_frames:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pixels = rgb_frame.reshape((-1, 3))
            all_pixels.extend(pixels)

        all_pixels = np.array(all_pixels)
        rgb_array = all_pixels / 255.0

        # Define the input and output whitepoints
        input_whitepoint = colour.RGB_COLOURSPACES['sRGB'].whitepoint
        output_whitepoint = colour.RGB_COLOURSPACES['ITU-R BT.709'].whitepoint

        # Perform chromatic adaptation from the input to the output whitepoint
        xyz_array = colour.RGB_to_XYZ(
            rgb_array,
            input_whitepoint,
            output_whitepoint,  # D65
            chromatic_adaptation_transform='Bradford'
        )

        # Convert from XYZ to the output color space
        input_color_space = np.clip(colour.XYZ_to_RGB(
            xyz_array,
            output_whitepoint,
            output_whitepoint,  # D65
            chromatic_adaptation_transform='Bradford'
        ), 0, 1)

        self.plot_color_spaces(input_color_space)
    
    def plot_color_spaces(self, input_color_space):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        if self.rec709CheckBox.isChecked():
            self.plot_color_space(ax, colour.RGB_COLOURSPACES['ITU-R BT.709'].primaries, 'Rec. 709')

        if self.inputColorCheckBox.isChecked() and input_color_space.size > 0:
            out_of_bounds = (input_color_space[:, 0] > 1) | (input_color_space[:, 1] > 1) | (input_color_space[:, 2] > 1)
            within_bounds = ~out_of_bounds

            ax.scatter(
                input_color_space[within_bounds, 0] * 100,
                input_color_space[within_bounds, 1] * 100,
                input_color_space[within_bounds, 2] * 100,
                c=input_color_space[within_bounds],
                marker='o',
                label='Input Color Space'
            )

            ax.scatter(
                input_color_space[out_of_bounds, 0] * 100,
                input_color_space[out_of_bounds, 1] * 100,
                input_color_space[out_of_bounds, 2] * 100,
                c='black',  # Set to black for visibility
                marker='x',
                label='Out of Bounds'
            )

        ax.set_xlabel('R')
        ax.set_ylabel('G')
        ax.set_zlabel('B')
        ax.legend(loc='upper right')
        self.canvas.draw()

    def plot_color_space(self, ax, primaries, label):
        vertices = np.array([
            primaries[0],
            primaries[1],
            primaries[2],
            primaries[0],
        ])
        vertices = np.hstack((vertices, np.zeros((vertices.shape[0], 1))))
        ax.plot(vertices[:, 0] * 100, vertices[:, 1] * 100, vertices[:, 2] * 100, label=label)

    def updatePlot(self):
        if self.filePath and self.inputColorCheckBox.isChecked():
            self.analyzeColorSpace()
        else:
            self.plot_color_spaces(np.array([]))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ColorSpaceAnalyzer()
    ex.show()
    sys.exit(app.exec_())
