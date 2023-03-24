import os
import csv
import sys
from typing import Callable

from PySide6.QtCore    import Qt, QItemSelection
from PySide6.QtGui     import QDragEnterEvent, QDropEvent, QColor, QBrush
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel,
    QGridLayout, QHBoxLayout, QVBoxLayout,
    QSpacerItem,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox,
    QPushButton, QRadioButton,
    QSpinBox, QDoubleSpinBox,
    QFileDialog, QDialogButtonBox,
    QAbstractItemView, QSizePolicy
)

from log.log import LogStream

import const

class EditPopup(QDialog):
    _editRowNum = -1
    _deleteReject = False
    def __init__(self,
        log: LogStream,
        setItem:   Callable[[int, int, QTableWidgetItem], None],
        removeRow: Callable[[int], None],
        parent=None):

        super().__init__(parent)
        self.log = log
        self._removeRow = removeRow
        self._setItem = setItem
        self.resize(400, 200)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Edit')
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout = QGridLayout()

        self.label = QLabel(self)
        self.label.setText('Reservoir')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self)
        self.label_2.setText('Flow Rate (uL/min)')
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.label_3 = QLabel(self)
        self.label_3.setText('Duration (ms)')
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.radioButton_None = QRadioButton(self)
        self.radioButton_None.setChecked(True)
        self.radioButton_None.setText(const.RESERVOIR_NAMES[0])
        self.gridLayout.addWidget(self.radioButton_None, 0, 1, 1, 1)

        self.radioButton_1 = QRadioButton(self)
        self.radioButton_1.setText(const.RESERVOIR_NAMES[1])
        self.gridLayout.addWidget(self.radioButton_1, 1, 1, 1, 1)

        self.radioButton_2 = QRadioButton(self)
        self.radioButton_2.setText(const.RESERVOIR_NAMES[2])
        self.gridLayout.addWidget(self.radioButton_2, 2, 1, 1, 1)

        self.radioButton_3 = QRadioButton(self)
        self.radioButton_3.setText(const.RESERVOIR_NAMES[3])
        self.gridLayout.addWidget(self.radioButton_3, 3, 1, 1, 1)

        self.radioButton_4 = QRadioButton(self)
        self.radioButton_4.setText(const.RESERVOIR_NAMES[4])
        self.gridLayout.addWidget(self.radioButton_4, 4, 1, 1, 1)

        self.flow_rate = QDoubleSpinBox(self)
        self.flow_rate.setSingleStep(0.01)
        self.flow_rate.setRange(0.0, const.FLOW_RATE_MAX)
        self.gridLayout.addWidget(self.flow_rate, 6, 1, 1, 1)

        self.duration = QSpinBox(self)
        self.duration.setRange(0, const.DURATION_MAX)
        self.duration.setSingleStep(10)
        self.gridLayout.addWidget(self.duration, 7, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok
        )

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def popup(self, editRowNum: int, deleteReject: bool):
        self._editRowNum = editRowNum
        self._deleteReject = deleteReject
        self.show()

    def validEditRow(self):
        if self._editRowNum < 0:
            self.log.debug("Bad row")
            sys.exit(1)
        return self._editRowNum

    def accept(self) -> None:
        if self.radioButton_1.isChecked():
            r = 1
        elif self.radioButton_2.isChecked():
            r = 2
        elif self.radioButton_3.isChecked():
            r = 3
        elif self.radioButton_4.isChecked():
            r = 4
        else:
            r = 0
        r = const.RESERVOIR_NAMES[r]
        self._setItem(self.validEditRow(), 0, QTableWidgetItem(r))
        f = f'{self.flow_rate.value():.2f}'
        self._setItem(self.validEditRow(), 1, QTableWidgetItem(f))
        t = str(self.duration.value())
        self._setItem(self.validEditRow(), 2, QTableWidgetItem(t))

        self._setItem(self.validEditRow(), 3, QTableWidgetItem(const.STATUS_PENDING))

        self._editRowNum = -1
        self._deleteReject = False
        return super().accept()

    def reject(self) -> None:
        if self._deleteReject:
            self._removeRow(self.validEditRow())

        self._editRowNum = -1
        self._deleteReject = False
        return super().reject()

class Table(QFrame):

    def __init__(self, log: LogStream, parent=None):
        super().__init__(parent)

        self.log = log

        self.resize(500, 300)
        self.setAcceptDrops(True)

        self.gridLayout = QGridLayout(self)

        self.horizontalLayout = QHBoxLayout()

        self.table = QTableWidget(self)
        if self.table.columnCount() < const.TABLE_COL:
            self.table.setColumnCount(const.TABLE_COL)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Reservoir'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Flow Rate (uL/min)'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Duration (ms)'))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem('Status'))
        self.table.horizontalHeader().setMinimumSectionSize(const.TABLE_WID)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setMinimumWidth(24+const.TABLE_WID*const.TABLE_COL)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self.onSelectionChange)
        self.horizontalLayout.addWidget(self.table)

        self.editPopup = EditPopup(
            log=self.log,
            setItem=self.table.setItem,
            removeRow=self.table.removeRow
        )

        self.verticalLayout = QVBoxLayout()

        self.buttonLoad = QPushButton(self)
        self.buttonLoad.setText('&Load')
        self.buttonLoad.clicked.connect(self.loadFile)
        self.verticalLayout.addWidget(self.buttonLoad)

        self.buttonSave = QPushButton(self)
        self.buttonSave.setText('&Save')
        self.buttonSave.clicked.connect(self.saveFile)
        self.verticalLayout.addWidget(self.buttonSave)

        self.verticalSpacer = QSpacerItem(
            20, 40,
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonNew = QPushButton(self)
        self.buttonNew.setText('&New')
        self.buttonNew.clicked.connect(self.newRow)
        self.verticalLayout.addWidget(self.buttonNew)

        self.buttonEdit = QPushButton(self)
        self.buttonEdit.setText('&Edit')
        self.buttonEdit.clicked.connect(self.editRow)
        self.verticalLayout.addWidget(self.buttonEdit)

        self.buttonDelete = QPushButton(self)
        self.buttonDelete.setText('&Delete')
        self.buttonDelete.clicked.connect(self.deleteRow)
        self.verticalLayout.addWidget(self.buttonDelete)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40,
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonUp = QPushButton(self)
        self.buttonUp.setText('&Up')
        self.buttonUp.clicked.connect(self.upRow)
        self.verticalLayout.addWidget(self.buttonUp)

        self.buttonDown = QPushButton(self)
        self.buttonDown.setText('D&own')
        self.buttonDown.clicked.connect(self.downRow)
        self.verticalLayout.addWidget(self.buttonDown)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.setButtonsSelection(False)

    def setButtonsSelection(self, b: bool):
        self.buttonEdit.setEnabled(b)
        self.buttonDelete.setEnabled(b)
        self.buttonUp.setEnabled(b)
        self.buttonDown.setEnabled(b)

    def setButtonsOthers(self, b: bool):
        self.buttonLoad.setEnabled(b)
        self.buttonSave.setEnabled(b)
        self.buttonNew.setEnabled(b)

    def setButtons(self, b: bool):
        self.setButtonsOthers(b)
        self.setButtonsSelection(b)

    def antifreeze(self):
        self.setButtonsOthers(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def freeze(self):
        self.setButtonsOthers(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def selectFrozen(self, row):
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.selectRow(row)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def onSelectionChange(self, selected: QItemSelection, deselected: QItemSelection):
        idx = selected.indexes()
        self.setButtonsSelection(len(idx) > 0)

    def newRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            ed = 1+idx[0].row()
        else:
            ed = self.table.rowCount()
        self.table.insertRow(ed)
        self.editPopup.flow_rate.setValue(0.0)
        self.editPopup.duration.setValue(0)
        self.editPopup.popup(ed, True)

    def editRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            ed = idx[0].row()
            r = self.table.item(ed, 0).text()
            if r == const.RESERVOIR_NAMES[0]:
                self.editPopup.radioButton_None.setChecked(True)
            elif r == const.RESERVOIR_NAMES[1]:
                self.editPopup.radioButton_1.setChecked(True)
            elif r == const.RESERVOIR_NAMES[2]:
                self.editPopup.radioButton_2.setChecked(True)
            elif r == const.RESERVOIR_NAMES[3]:
                self.editPopup.radioButton_3.setChecked(True)
            elif r == const.RESERVOIR_NAMES[4]:
                self.editPopup.radioButton_4.setChecked(True)
            else:
                self.log.warn(f'Row {ed}: unknown reservoir')

            try:
                f = float(self.table.item(ed, 1).text())
            except ValueError:
                self.log.warn(f'Row {ed}: unknown flow rate')
                f = 0.0
            self.editPopup.flow_rate.setValue(f)

            try:
                t = int(self.table.item(ed, 2).text())
            except ValueError:
                self.log.warn(f'Row {ed}: unknown duration')
                t = 0
            self.editPopup.duration.setValue(t)
            self.editPopup.popup(ed, False)

    def deleteRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            self.table.removeRow(idx[0].row())
            idx = self.table.selectionModel().selectedRows()
            if len(idx) > 0:
                self.table.selectRow(idx[0].row())

    def moveRow(self, row_upper: int):
        if 0 <= row_upper < self.table.rowCount()-1:
            for i in [0, 1, 2]:
                a = self.table.takeItem(row_upper, i)
                b = self.table.takeItem(row_upper+1, i)
                self.table.setItem(row_upper+1, i, a)
                self.table.setItem(row_upper, i, b)

    def upRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            ed = idx[0].row()
            self.moveRow(ed-1)
            if 0 < ed < self.table.rowCount():
                self.table.selectRow(ed-1)
            else:
                self.table.selectRow(ed)

    def downRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            ed = idx[0].row()
            self.moveRow(ed)
            if 0 < (ed+1) < self.table.rowCount():
                self.table.selectRow(ed+1)
            else:
                self.table.selectRow(ed)

    def updateRow(self, row: int) -> tuple[bool, str, float, int]:
        if row > 0:
            item = QTableWidgetItem(const.STATUS_DONE)
            item.setForeground(QBrush(QColor(0, 255, 0)))
            self.table.setItem(row-1, 3, item)
        if row >= self.table.rowCount():
            return (False, "None", 0.0, 0)
        self.table.setItem(row, 3, QTableWidgetItem(const.STATUS_RUNNING))
        res = self.table.item(row, 0).text()
        flo = float(self.table.item(row, 1).text())
        msec = int(self.table.item(row, 2).text())
        return (True, res, flo, msec)

    def resetStatus(self):
        for i in range(self.table.rowCount()):
            self.table.setItem(i, 3, QTableWidgetItem(const.STATUS_PENDING))

    def loadFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open File",
            "", "CSV File (*.csv)"
        )
        if len(file) > 0:
            self.loadCSV(file)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText() and _isCSV(event.mimeData().text()):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        url: str = event.mimeData().text()
        self.loadCSV(_noPre('file:///', url))

    def loadCSV(self, name: str):
        self.table.setRowCount(0)
        errors = 0

        with open(name, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                r = self.table.rowCount()
                err, row = self.checkCSV(name, r, row)
                errors += err

                self.table.insertRow(r)
                self.table.setItem(r, 3, QTableWidgetItem(const.STATUS_PENDING))
                for i in range(const.CSV_LEN):
                    self.table.setItem(r, i, QTableWidgetItem(row[i]))
        if errors == 0:
            self.log.info(f'Loaded file "{name}"')
        else:
            self.log.error(f'Loaded file "{name}" with {errors} error(s)')
            QMessageBox.critical(self, "Error",
                f'Loaded file "{name}" with {errors} error(s)')


    def checkCSV(self, name: str, r: int, row: list[str]) -> tuple[int, list[str]]:
        err = 0

        if len(row) != const.CSV_LEN:
            self.log.error(f'File "{name}", line {1+r}: wrong number of values')
            return 1, [const.RESERVOIR_NAMES[0], str(0.0), str(0)]

        res = row[0]
        if res not in const.RESERVOIR_NAMES:
            self.log.error(
                f'File "{name}", line {1+r}: unknown reservoir name "{res}"')
            res = const.RESERVOIR_NAMES[0]
            err += 1

        flo = row[1]
        try:
            f = float(flo)
            if not 0.0 <= f <= const.FLOW_RATE_MAX:
                raise ValueError
        except ValueError:
            self.log.error(f'File "{name}", line {1+r}: bad flow rate "{flo}"')
            flo = str(0.0)
            err += 1

        msec = row[2]
        try:
            i = int(msec)
            if not 0 <= i <= const.DURATION_MAX:
                raise ValueError
        except ValueError:
            self.log.error(f'File "{name}", line {1+r}: bad duration "{msec}"')
            msec = str(0)
            err += 1

        return err, [res, flo, msec]

    def saveFile(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save File",
            "", "CSV File (*.csv)"
        )
        if len(file) > 0:
            self.saveCSV(file)

    def saveCSV(self, name: str):
        row = self.table.rowCount()
        with open(name, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for i in range(row):
                writer.writerow([
                    self.table.item(i, j).text() for j in range(const.CSV_LEN)
                ])

        self.log.info(f'Saved as file  "{name}"')

def _isCSV(url: str) -> bool:
    ext = os.path.splitext(url)[1]
    return ext == '.csv'

def _noPre(prefix: str, text: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
