from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import sys
from typing import List

class EditPopup(QDialog):
    def __init__(self, parent=None):
        super(EditPopup, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Edit')
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText('Reagent')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText('Flow Rate (uL/min)')
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.label_3 = QLabel(self)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setText('Time (sec)')
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.radioButton_None = QRadioButton(self)
        self.radioButton_None.setObjectName(u"radioButton_None")
        self.radioButton_None.setChecked(True)
        self.radioButton_None.setText('None')
        self.gridLayout.addWidget(self.radioButton_None, 0, 1, 1, 1)

        self.radioButton_1 = QRadioButton(self)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setText('1')
        self.gridLayout.addWidget(self.radioButton_1, 1, 1, 1, 1)
        
        self.radioButton_2 = QRadioButton(self)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setText('2')
        self.gridLayout.addWidget(self.radioButton_2, 2, 1, 1, 1)

        self.radioButton_3 = QRadioButton(self)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setText('3')
        self.gridLayout.addWidget(self.radioButton_3, 3, 1, 1, 1)

        self.radioButton_4 = QRadioButton(self)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setText('4')
        self.gridLayout.addWidget(self.radioButton_4, 4, 1, 1, 1)

        self.doubleSpinBox = QDoubleSpinBox(self)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 6, 1, 1, 1)

        self.spinBox = QSpinBox(self)
        self.spinBox.setObjectName(u"spinBox")
        self.gridLayout.addWidget(self.spinBox, 7, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


def _lastOf(x: List[QModelIndex]):
    return x[len(x)-1].row()

class TableForm(QFrame):
    
    def __init__(self, parent=None):
        super(TableForm, self).__init__(parent)

        self.resize(500, 300)

        self.editPopup = EditPopup()

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        self.table = QTableWidget(self)
        if (self.table.columnCount() < 3):
            self.table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem('Reagent')
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem('Flow Rate')
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem('Time')
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table.setObjectName(u"table")
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.horizontalLayout.addWidget(self.table)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        self.buttonLoad = QPushButton(self)
        self.buttonLoad.setObjectName(u"buttonLoad")
        self.buttonLoad.setText('&Load')
        self.verticalLayout.addWidget(self.buttonLoad)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonNew = QPushButton(self)
        self.buttonNew.setObjectName(u"buttonNew")
        self.buttonNew.setText('&New')
        self.buttonNew.clicked.connect(self.newRow)
        self.verticalLayout.addWidget(self.buttonNew)

        self.buttonEdit = QPushButton(self)
        self.buttonEdit.setObjectName(u"buttonEdit")
        self.buttonEdit.setText('&Edit')
        self.verticalLayout.addWidget(self.buttonEdit)

        self.buttonDelete = QPushButton(self)
        self.buttonDelete.setObjectName(u"buttonDelete")
        self.buttonDelete.setText('&Delete')
        self.verticalLayout.addWidget(self.buttonDelete)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonUp = QPushButton(self)
        self.buttonUp.setObjectName(u"buttonUp")
        self.buttonUp.setText('&Up')
        self.verticalLayout.addWidget(self.buttonUp)

        self.buttonDown = QPushButton(self)
        self.buttonDown.setObjectName(u"buttonDown")
        self.buttonDown.setText('D&own')
        self.verticalLayout.addWidget(self.buttonDown)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

    def setButtons(self, b: bool):
        self.buttonLoad.setEnabled(b)
        self.buttonNew.setEnabled(b)
        self.buttonEdit.setEnabled(b)
        self.buttonDelete.setEnabled(b)
        self.buttonUp.setEnabled(b)
        self.buttonDown.setEnabled(b)
    
    def setButtonsEnabled(self):
        self.setButtons(True)

    def setButtonsDisabled(self):
        self.setButtons(False)

    def newRow(self):
        idx = self.table.selectionModel().selectedRows()
        if len(idx) > 0:
            self.table.insertRow(1+_lastOf(idx))
        else:
            self.table.insertRow(self.table.rowCount())
        self.editPopup.show()
    

# for testing
def main():
    app = QApplication(sys.argv)
    form = TableForm()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


