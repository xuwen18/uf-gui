from PySide6.QtCore    import *
from PySide6.QtGui     import *
from PySide6.QtWidgets import *

import os
import csv
from typing import Callable

class EditPopup(QDialog):
    _edit_row = -1
    _delete_reject = False
    def __init__(self, 
        setItem:   Callable[[int, int, QTableWidgetItem], None], 
        removeRow: Callable[[int], None], 
        parent=None):
        
        super().__init__(parent)
        self._removeRow = removeRow
        self._setItem = setItem
        self.resize(400, 200)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Edit')
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout = QGridLayout()
        
        self.label = QLabel(self)
        self.label.setText('Reagent')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self)
        self.label_2.setText('Flow Rate (uL/min)')
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.label_3 = QLabel(self)
        self.label_3.setText('Time (sec)')
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.radioButton_None = QRadioButton(self)
        self.radioButton_None.setChecked(True)
        self.radioButton_None.setText('None')
        self.gridLayout.addWidget(self.radioButton_None, 0, 1, 1, 1)

        self.radioButton_1 = QRadioButton(self)
        self.radioButton_1.setText('1')
        self.gridLayout.addWidget(self.radioButton_1, 1, 1, 1, 1)
        
        self.radioButton_2 = QRadioButton(self)
        self.radioButton_2.setText('2')
        self.gridLayout.addWidget(self.radioButton_2, 2, 1, 1, 1)

        self.radioButton_3 = QRadioButton(self)
        self.radioButton_3.setText('3')
        self.gridLayout.addWidget(self.radioButton_3, 3, 1, 1, 1)

        self.radioButton_4 = QRadioButton(self)
        self.radioButton_4.setText('4')
        self.gridLayout.addWidget(self.radioButton_4, 4, 1, 1, 1)

        self.flow_rate = QDoubleSpinBox(self)
        self.flow_rate.setSingleStep(0.01)
        self.gridLayout.addWidget(self.flow_rate, 6, 1, 1, 1)

        self.time = QSpinBox(self)
        self.time.setRange(0, 100000)
        self.time.setSingleStep(10)
        self.gridLayout.addWidget(self.time, 7, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok
        )

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def popup(self, edit_row: int, delete_reject: bool):
        self._edit_row = edit_row
        self._delete_reject = delete_reject
        self.show()

    def validEditRow(self):
        assert self._edit_row != -1 #TODO: handle properly
        return self._edit_row
    
    def accept(self) -> None:
        if self.radioButton_1.isChecked():
            r = '1'
        elif self.radioButton_2.isChecked():
            r = '2'
        elif self.radioButton_3.isChecked():
            r = '3'
        elif self.radioButton_4.isChecked():
            r = '4'
        else:
            r = 'None'
        self._setItem(self.validEditRow(), 0, QTableWidgetItem(r))
        f = f'{self.flow_rate.value():.2f}'
        self._setItem(self.validEditRow(), 1, QTableWidgetItem(f))
        t = str(self.time.value())
        self._setItem(self.validEditRow(), 2, QTableWidgetItem(t))
       
        self._edit_row = -1
        self._delete_reject = False
        return super().accept()

    def reject(self) -> None:
        if self._delete_reject:
            self._removeRow(self.validEditRow())
        
        self._edit_row = -1
        self._delete_reject = False
        return super().reject()

class Table(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(500, 300)
        self.setAcceptDrops(True)

        self.gridLayout = QGridLayout(self)
        
        self.horizontalLayout = QHBoxLayout()
        
        self.table = QTableWidget(self)
        if (self.table.columnCount() < 3):
            self.table.setColumnCount(3)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Reagent'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Flow Rate'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Time'))
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self.onSelectionChange)
        self.horizontalLayout.addWidget(self.table)

        self.editPopup = EditPopup(
            setItem=self.table.setItem, 
            removeRow=self.table.removeRow
        )

        self.verticalLayout = QVBoxLayout()
        
        self.buttonLoad = QPushButton(self)
        self.buttonLoad.setText('&Load')
        self.buttonLoad.clicked.connect(self.loadFile)
        self.verticalLayout.addWidget(self.buttonLoad)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
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

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
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

    def setButtons(self, b: bool):
        self.buttonLoad.setEnabled(b)
        self.buttonNew.setEnabled(b)
        self.setButtonsSelection(b)
    
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
        self.editPopup.time.setValue(0)
        self.editPopup.popup(ed, True)
    
    def editRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            ed = idx[0].row()
            r = self.table.item(ed, 0).text()
            if r == '1':
                self.editPopup.radioButton_1.setChecked(True)
            elif r == '2':
                self.editPopup.radioButton_2.setChecked(True)
            elif r == '3':
                self.editPopup.radioButton_3.setChecked(True)
            elif r == '4':
                self.editPopup.radioButton_4.setChecked(True)
            else:
                self.editPopup.radioButton_None.setChecked(True)
            # TODO: handle errors
            try:
                f = float(self.table.item(ed, 1).text())
            except:
                f = 0.0
            self.editPopup.flow_rate.setValue(f)
            try:
                t = int(self.table.item(ed, 2).text())
            except:
                t = 0
            self.editPopup.time.setValue(t)
            self.editPopup.popup(ed, False)
    
    def deleteRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            self.table.removeRow(idx[0].row())
            idx = self.table.selectionModel().selectedRows()
            if len(idx) > 0:
                self.table.selectRow(idx[0].row())

    def moveRow(self, row_upper: int):
        if row_upper >= 0 and row_upper+1 < self.table.rowCount():
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
            if ed > 0 and ed < self.table.rowCount():
                self.table.selectRow(ed-1)
            else:
                self.table.selectRow(ed)
    
    def downRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            ed = idx[0].row()
            self.moveRow(ed)
            if ed+1 > 0 and ed+1 < self.table.rowCount():
                self.table.selectRow(ed+1)
            else:
                self.table.selectRow(ed)

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
        with open(name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                r = self.table.rowCount()
                self.table.insertRow(r)
                assert len(row) == 3
                for i in [0, 1, 2]:
                    self.table.setItem(r, i, QTableWidgetItem(row[i]))


def _isCSV(url: str) -> bool:
    ext = os.path.splitext(url)[1]
    return ext == '.csv'

def _noPre(prefix: str, text: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

# for testing
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Table()
    form.show()
    sys.exit(app.exec())


