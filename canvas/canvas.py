from PySide6.QtCore    import QTimer
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QApplication
)

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    # NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure    import Figure

from typing import Callable
import numpy as np


class Canvas(QFrame):

    def __init__(self,
        getData: Callable[[int], float],
        interval=1000,
        width=5, height=4,
        parent=None
    ):
        super().__init__(parent)
        self.getData = getData

        self.i = 0
        self.x = np.zeros(200)
        self.y = np.zeros(200)

        self.timer = QTimer(self)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.animate)

        fig = Figure(figsize=(width, height))
        self.fc = FigureCanvasQTAgg(figure=fig)
        self.ax = fig.add_subplot()

        layout = QVBoxLayout()
        #toolbar = NavigationToolbar(self.fc, self)
        #layout.addWidget(toolbar)
        layout.addWidget(self.fc)
        self.setLayout(layout)

    def animate(self):
        i = self.i
        pt = self.getData(i)
        self.x = np.append(self.x[1:], i)
        self.y = np.append(self.y[1:], pt)

        self.ax.clear()
        self.ax.plot(self.x, self.y)
        self.fc.draw()

        self.i += 1

if __name__ == "__main__":
    import sys
    import math
    app = QApplication(sys.argv)
    c = Canvas(lambda i: math.cos(0.1 * i))
    c.timer.start()
    c.show()
    sys.exit(app.exec())
