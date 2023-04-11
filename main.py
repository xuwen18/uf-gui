import sys

import parse

from PySide6.QtCore    import Qt, QRect, QByteArray, QElapsedTimer, QIODevice
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout,
    QLabel, QHBoxLayout, QPushButton, QSpacerItem,
    QSizePolicy, QMenuBar, QStatusBar,
    QDockWidget,
    QApplication
)

from canvas.canvas import Canvas
from table.table   import Table
from port.port     import PortDialog
from log.log       import Logger, LogStream
from runner.runner import Runner

import const

class MainWindow(QMainWindow):
    serial = None

    buffer = QByteArray(b"")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1280, 720)
        self.centralwidget = QWidget(self)

        self.gridLayout = QGridLayout(self.centralwidget)

        self.tab3 = QWidget()
        self.gridLayout3 = QGridLayout(self.tab3)
        self.logger = Logger(parent=self)
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

        self.labelDuration = QLabel(self.tab2)
        self.gridLayout2.addWidget(self.labelDuration, 4, 0, 1, 1)
        self.dataDuration = QLabel(self.tab2)
        self.dataDuration.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.gridLayout2.addWidget(self.dataDuration, 4, 1, 1, 1)

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

        self.gridLayout2.addLayout(self.horizontalLayout, 5, 0, 1, 2)

        self.gridLayout.addWidget(self.tab2, 0, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.dock1 = QDockWidget("", self)
        self.dock1.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)
        self.dock1.setWidget(self.tab1)
        self.dock3 = QDockWidget("", self)
        self.dock3.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock3)
        self.dock3.setWidget(self.tab3)

        self.setWindowTitle('Microfluidics Control Program')
        self.dock1.setWindowTitle("Commands")
        self.dock3.setWindowTitle("Logs")
        self.labelReservoir.setText('Reservoir: ')
        self.labelFlow.setText('Flow rate (uL/min): ')
        self.labelPressure.setText('Pressure (psi): ')
        self.labelDuration.setText('Elapsed time (ms): ')
        self.labelPort.setText('')
        self.buttonConnect.setText('&Connect')
        self.buttonStart.setText('&Start')
        self.showData("None", 0.0, 0.0, 0)

        #self.buttonStart.setEnabled(False)

        self.log.debug("GUI started")

        self.timer = QElapsedTimer()
        self.is_running = False

        self.runner = Runner(
            self, self.start, self.stop,
            self.table.updateRow, self.sendText
        )

    def showData(self, numReservoir, flowRate, pressure, duration):
        self.dataReservoir.setText(f'{numReservoir}')
        self.dataFlow.setText(f'{flowRate:.3f}')
        self.dataPressure.setText(f'{pressure:.3f}')
        self.dataDuration.setText(f'{duration}')

    def stop(self):
        # self.table.antifreeze()
        self.log.info('Stopped')
        self.buttonStart.setText('&Start')
        self.i = 0
        self.is_running = False
        self.serial.readyRead.disconnect(self.onReadyRead)

    def start(self):
        # self.table.freeze()
        # self.table.selectFrozen(0)
        self.timer.start()
        self.log.info('Started')
        self.buttonStart.setText('&Stop')
        self.table.resetStatus()
        self.canvas.reset()
        self.is_running = True
        self.serial.readyRead.connect(self.onReadyRead)

    def onRun(self):
        if self.is_running:
            self.runner.reset()
        else:
            self.runner.begin()

    def onReadyRead(self):
        self.buffer.append(self.serial.readAll())
        idx_l = self.buffer.lastIndexOf(b"[")
        idx_r = self.buffer.lastIndexOf(b"]")
        if idx_l != -1 and idx_r != -1 and idx_l < idx_r:
            qba = self.buffer.mid(1+idx_l, idx_r-idx_l-1)
            msg = qba.data().decode()
            rslt = parse.parse('{:d},{:g}', msg)
            if rslt is None:
                self.log.error("Something wrong")
                return
            reservoir = rslt[0]
            flowRate = rslt[1]
            pressure = 0 # unknown
            dur = self.timer.elapsed()
            self.canvas.animate(dur, flowRate, self.runner.current_flo)
            self.showData(reservoir,flowRate, pressure, dur)
            self.log.info(f'Serial read "{msg}"')

    def onConnect(self):
        serial = PortDialog.getSerial(self)
        if serial is not None:
            name = serial.portName()
            if self.serial is not None:
                self.serial.close()
            if serial.open(QIODevice.OpenModeFlag.ReadWrite):
                self.serial = serial
                self.labelPort.setText(name)
                self.log.info(f"Serial connected: {name}")

                #self.buttonStart.setEnabled(True)
            else:
                self.serial = None
                self.log.error(f'Failed to open serial port: {name}')

                #self.buttonStart.setEnabled(False)

    def sendText(self, text: str):
        self.log.debug(f'Serial sent text "{text}"')
        if self.serial is not None:
            qba = QByteArray(text.encode("utf-8"))
            self.serial.write(qba)

    def closeEvent(self, event):
        if self.serial is not None:
            self.serial.close()
        self.log.debug("GUI closing")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
