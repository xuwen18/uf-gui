from PySide6.QtCore    import *
from PySide6.QtGui     import *
from PySide6.QtWidgets import *

from canvas.canvas import Canvas
from table.table   import Table
from port.port     import PortDialog

import sys
import math

class MainWindow(QMainWindow):
    serial = None

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.centralwidget = QWidget(self)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.tabWidget = QTabWidget(self.centralwidget)
        
        self.tab1 = QWidget()
        self.gridLayout1 = QGridLayout(self.tab1)
        self.table = Table(self.tab1)
        self.gridLayout1.addWidget(self.table, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, "")

        self.tab2 = QWidget()
        self.gridLayout2 = QGridLayout(self.tab2)
        self.canvas = Canvas(getData=lambda i: math.cos(0.1*i), parent=self)
        self.gridLayout2.addWidget(self.canvas, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "")
        
        self.labelReagent = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelReagent, 1, 0, 1, 1)

        self.labelFlow = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelFlow, 2, 0, 1, 1)

        self.labelPressure = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelPressure, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()

        self.buttonConnect = QPushButton(self.tab2)
        self.buttonConnect.clicked.connect(self.onConnect)
        self.horizontalLayout.addWidget(self.buttonConnect)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonStart = QPushButton(self.tab2)
        self.horizontalLayout.addWidget(self.buttonStart)

        self.buttonPause = QPushButton(self.tab2)
        self.horizontalLayout.addWidget(self.buttonPause)

        self.gridLayout2.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.tabWidget.setCurrentIndex(1)

        self.setWindowTitle('Microfluidics Control Program')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), 'Commands')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), 'Main')
        self.labelReagent.setText('Reagent: ')
        self.labelFlow.setText('Flow rate: ')
        self.labelPressure.setText('Pressure: ')
        self.buttonConnect.setText('&Connect')
        self.buttonStart.setText('&Start')
        self.buttonPause.setText('&Pause')
    
    def onConnect(self):
        serial = PortDialog.getSerial(self)
        if serial is not None:
            self.serial = serial

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
