from typing import Optional

from PySide6.QtGui        import Qt, QAction
from PySide6.QtWidgets    import (
    QApplication, QDialog, QLabel, QMenu,
    QGridLayout, QHBoxLayout,
    QPushButton, QDialogButtonBox,
)
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


class PortDialog(QDialog):
    selected_port: Optional[str] = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(300, 100)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Connect port')

        self.gridLayout = QGridLayout(self)
        self.horizontalLayout = QHBoxLayout()

        self.label = QLabel(self)
        self.horizontalLayout.addWidget(self.label)

        self.buttonConnect = QPushButton(self)
        self.horizontalLayout.addWidget(self.buttonConnect)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.label.setText('Connect port')
        self.buttonConnect.setText('search...')

        serial_list = QSerialPortInfo.availablePorts()
        ports_menu = QMenu(self.buttonBox)
        ports_menu.triggered.connect(self.selectPort)
        for port in serial_list:
            ports_menu.addAction(port.portName())

        self.buttonConnect.setMenu(ports_menu)

    def selectPort(self, action: QAction):
        self.selected_port = action.text()
        self.buttonConnect.setText(self.selected_port)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)

    def reject(self) -> None:
        self.selected_port = None
        return super().reject()

    @staticmethod
    def getSerial(parent = None) -> Optional[QSerialPort]:
        dialog = PortDialog(parent)
        dialog.exec()
        if dialog.selected_port is None:
            return None
        return QSerialPort(
            dialog.selected_port, parent,
            baudRate=QSerialPort.BaudRate.Baud115200
        )


# for testing
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = PortDialog()
    form.show()
    sys.exit(app.exec())


