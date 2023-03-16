from PySide6.QtWidgets import (
    QFrame, QVBoxLayout
)

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
)
from matplotlib.figure import Figure

import numpy as np


class Canvas(QFrame):

    def __init__(self, length=50, width=5, height=4, parent=None):
        super().__init__(parent)

        self.x1 = np.zeros(length)
        self.y1 = np.zeros(length)
        self.y2 = np.zeros(length)

        fig = Figure(figsize=(width, height))
        self.fc = FigureCanvasQTAgg(figure=fig)
        self.ax = fig.add_subplot()

        layout = QVBoxLayout()
        layout.addWidget(self.fc)
        self.setLayout(layout)

    def animate(self, nextX1, nextY1, nextY2):
        self.x1 = np.append(self.x1[1:], nextX1)
        self.y1 = np.append(self.y1[1:], nextY1)
        self.y2 = np.append(self.y2[1:], nextY2)

        self.ax.clear()
        self.ax.plot(self.x1, self.y1)
        self.ax.plot(self.x1, self.y2)
        self.fc.draw()
