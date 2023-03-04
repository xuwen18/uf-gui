import sys
# dummy
import random

from PySide6.QtCore    import Qt, QRect, QTimer
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

import const

class MainWindow(QMainWindow):
    serial = None

    def __init__(self, interval=1000, parent=None):
        super().__init__(parent)
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
        self.canvas = Canvas(parent=self)
        self.gridLayout2.addWidget(self.canvas, 0, 0, 1, 2)

        self.labelReservoir = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelReservoir, 1, 0, 1, 1)
        self.dataReservoir = QLabel(self.tab2)
        self.dataReservoir.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.gridLayout2.addWidget(self.dataReservoir, 1, 1, 1, 1)

        self.labelFlow = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelFlow, 2, 0, 1, 1)
        self.dataFlow = QLabel(self.tab2)
        self.dataFlow.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.gridLayout2.addWidget(self.dataFlow, 2, 1, 1, 1)

        self.labelPressure = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelPressure, 3, 0, 1, 1)
        self.dataPressure = QLabel(self.tab2)
        self.dataPressure.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.gridLayout2.addWidget(self.dataPressure, 3, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()

        self.buttonConnect = QPushButton(self.tab2)
        self.buttonConnect.clicked.connect(self.onConnect)
        self.horizontalLayout.addWidget(self.buttonConnect)

        self.labelPort = QLabel(self.tab2)
        self.horizontalLayout.addWidget(self.labelPort)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonStart = QPushButton(self.tab2)
        self.buttonStart.clicked.connect(self.onRun)
        self.horizontalLayout.addWidget(self.buttonStart)

        self.gridLayout2.addLayout(self.horizontalLayout, 4, 0, 1, 2)

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
        self.tabWidget.setTabText(0, 'Commands')
        self.tabWidget.setTabText(1, 'Main')
        self.tabWidget.setTabText(2, 'Logs')
        self.labelReservoir.setText('Reservoir: ')
        self.labelFlow.setText('Flow rate: ')
        self.labelPressure.setText('Pressure: ')
        self.labelPort.setText('')
        self.buttonConnect.setText('&Connect')
        self.buttonStart.setText('&Start')
        self.showData("None", 0.0, 0.0)

        self.log.debug("GUI started")

        self.timer = QTimer(self)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.onTimeout)
        self.i = 0

    def showData(self, numReservoir, flowRate, pressure):
        self.dataReservoir.setText(f'{numReservoir}')
        self.dataFlow.setText(f'{flowRate:.3f}')
        self.dataPressure.setText(f'{pressure:.3f}')

    def onRun(self):
        if self.timer.isActive():
            self.timer.stop()
            self.log.info('Stopped')
            self.buttonStart.setText('&Start')
        else:
            self.timer.start()
            self.log.info('Started')
            self.buttonStart.setText('&Pause')

    def onTimeout(self):
        flowRate = 80*random.random()
        pressure = 30*random.random()
        self.canvas.animate(self.i, flowRate)
        self.showData(
            random.choice(const.RESERVOIR_NAMES),
            flowRate, pressure)
        self.i += 1

    def onConnect(self):
        serial = PortDialog.getSerial(self)
        if serial is not None:
            self.serial = serial
            name = serial.portName()
            self.labelPort.setText(name)
            self.log.info(f"Serial connected: {name}")

    def closeEvent(self, event):
        self.log.debug("GUI closing")

app = QApplication(sys.argv)
w = MainWindow(500)
w.show()
app.exec()
