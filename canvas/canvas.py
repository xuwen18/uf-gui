from PySide6.QtCore    import QTimer
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QApplication
)

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
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
        toolbar = NavigationToolbar(self.fc, self)
        layout.addWidget(toolbar)
        layout.addWidget(self.fc)
        self.setLayout(layout)

    def animate(self, nextX, nextY):
        self.x = np.append(self.x[1:], nextX)
        self.y = np.append(self.y[1:], nextY)

        self.ax.clear()
        self.ax.plot(self.x, self.y)
        self.fc.draw()

if __name__ == "__main__":
    import sys
    import math
    app = QApplication(sys.argv)
    c = Canvas(lambda i: math.cos(0.1 * i))
    c.timer.start()
    c.show()
    sys.exit(app.exec())
