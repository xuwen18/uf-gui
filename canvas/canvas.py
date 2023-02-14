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

        self.x = np.zeros(length)
        self.y = np.zeros(length)

        fig = Figure(figsize=(width, height))
        self.fc = FigureCanvasQTAgg(figure=fig)
        self.ax = fig.add_subplot()

        layout = QVBoxLayout()
        layout.addWidget(self.fc)
        self.setLayout(layout)

    def animate(self, nextX, nextY):
        self.x = np.append(self.x[1:], nextX)
        self.y = np.append(self.y[1:], nextY)

        self.ax.clear()
        self.ax.plot(self.x, self.y)
        self.fc.draw()
