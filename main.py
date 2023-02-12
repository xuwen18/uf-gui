import sys
import math

from PySide6.QtCore    import QRect
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout, QTabWidget,
    QLabel, QHBoxLayout, QPushButton, QSpacerItem,
    QSizePolicy, QMenuBar, QStatusBar,
    QApplication
)

from canvas.canvas import Canvas
from table.table   import Table
from port.port     import PortDialog
from log.log       import Logger, LogStream


class MainWindow(QMainWindow):
    serial = None

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.centralwidget = QWidget(self)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.tabWidget = QTabWidget(self.centralwidget)

        self.tab3 = QWidget()
        self.gridLayout3 = QGridLayout(self.tab3)
        self.logger = Logger(True, parent=self)
        self.gridLayout3.addWidget(self.logger, 0, 0, 1, 1)
        self.log = LogStream()
        self.log.written.connect(self.logger.written)

        self.tab1 = QWidget()
        self.gridLayout1 = QGridLayout(self.tab1)
        self.table = Table(self.log, self.tab1)
        self.gridLayout1.addWidget(self.table, 0, 0, 1, 1)

        self.tab2 = QWidget()
        self.gridLayout2 = QGridLayout(self.tab2)
        self.canvas = Canvas(
            getData=lambda i: math.sin(0.1*i),
            parent=self
        )
        self.gridLayout2.addWidget(self.canvas, 0, 0, 1, 1)

        self.labelReservoir = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelReservoir, 1, 0, 1, 1)

        self.labelFlow = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelFlow, 2, 0, 1, 1)

        self.labelPressure = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelPressure, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()

        self.buttonConnect = QPushButton(self.tab2)
        self.buttonConnect.clicked.connect(self.onConnect)
        self.horizontalLayout.addWidget(self.buttonConnect)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonStart = QPushButton(self.tab2)
        self.buttonStart.clicked.connect(self.onRun)
        self.horizontalLayout.addWidget(self.buttonStart)

        self.gridLayout2.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.tabWidget.addTab(self.tab1, "")
        self.tabWidget.addTab(self.tab2, "")
        self.tabWidget.addTab(self.tab3, "")

        self.tabWidget.setCurrentIndex(1)

        self.setWindowTitle('Microfluidics Control Program')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), 'Commands')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), 'Main')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), 'Logs')
        self.labelReservoir.setText('Reservoir: ')
        self.labelFlow.setText('Flow rate: ')
        self.labelPressure.setText('Pressure: ')
        self.buttonConnect.setText('&Connect')
        self.buttonStart.setText('&Start')

        self.log.debug("GUI started")

    def onRun(self):
        if self.canvas.timer.isActive():
            self.canvas.timer.stop()
            self.log.info('paused')
            self.buttonStart.setText('&Start')
        else:
            self.canvas.timer.start()
            self.log.info('started')
            self.buttonStart.setText('&Pause')

    def onConnect(self):
        serial = PortDialog.getSerial(self)
        if serial is not None:
            self.serial = serial
            self.log.info(f"serial connected: {serial.portName()}")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
