import numpy as np

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtWidgets import QFrame, QVBoxLayout

import const

matplotlib.use('Qt5Agg')

class Canvas(QFrame):

    def __init__(self, length=const.DATA_LENGTH, parent=None):
        super().__init__(parent)
        self.length = length

        fig = Figure(layout='constrained')
        self.fc = FigureCanvasQTAgg(figure=fig)
        self.ax = fig.add_subplot()

        layout = QVBoxLayout()
        layout.addWidget(self.fc)
        self.setLayout(layout)

        self.reset()

    def reset(self):
        self.x1 = np.zeros(self.length)
        self.y1 = np.zeros(self.length)
        self.y2 = np.zeros(self.length)

        self.ax.set_xlabel(const.X_LABEL)
        self.ax.set_ylabel(const.Y_LABEL)
        self.ax.set_ylim(bottom=0)
        self.ax.grid()
        self.fc.draw()

    def animate(self, nextX1, nextY1, nextY2):
        self.x1 = np.append(self.x1[1:], nextX1)
        self.y1 = np.append(self.y1[1:], nextY1)
        self.y2 = np.append(self.y2[1:], nextY2)

        self.ax.clear()
        self.ax.plot(self.x1, self.y1)
        self.ax.plot(self.x1, self.y2)
        self.ax.set_xlabel(const.X_LABEL)
        self.ax.set_ylabel(const.Y_LABEL)
        self.ax.set_ylim(bottom=0)
        self.ax.grid()
        self.fc.draw()
