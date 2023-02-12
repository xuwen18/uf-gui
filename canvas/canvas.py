from PySide6.QtCore    import *
from PySide6.QtGui     import *
from PySide6.QtWidgets import *

from typing import List, Callable

import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    # NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure    import Figure
from matplotlib.animation import FuncAnimation


class Canvas(QFrame):
    x: List[float] = 200*[0.0]
    y: List[float] = 200*[0.0]

    def __init__(self, getData: Callable[[int], float], width=5, height=4, parent=None):
        super().__init__(parent)
        self.getData = getData

        fig = Figure(figsize=(width, height))
        self.fc = FigureCanvasQTAgg(figure=fig)
        self.ax = fig.add_subplot()
        self.ani = FuncAnimation(fig, self.animate, frames=None, interval=100, repeat=False)

        layout = QVBoxLayout()
        #toolbar = NavigationToolbar(self.fc, self)
        #layout.addWidget(toolbar)
        layout.addWidget(self.fc)
        self.setLayout(layout)

    def animate(self, i):
        pt = self.getData(i)
        self.x.pop(0)
        self.x.append(i)
        self.y.pop(0)
        self.y.append(pt)

        self.ax.clear()
        self.ax.plot(self.x, self.y)

if __name__ == "__main__":
    import sys
    import math
    app = QApplication(sys.argv)
    c = Canvas(lambda i: math.cos(0.1 * i))
    c.show()
    sys.exit(app.exec())


