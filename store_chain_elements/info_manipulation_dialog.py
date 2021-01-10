from typing import Tuple, Union

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets


class Ui_InfoManipulationDialog:
    def setupUi(self, InfoManipulationDialog):
        InfoManipulationDialog.setObjectName("InfoManipulationDialog")
        InfoManipulationDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(InfoManipulationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.optionLayout = QtWidgets.QFormLayout()
        self.optionLayout.setObjectName("optionLayout")
        self.verticalLayout.addLayout(self.optionLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(InfoManipulationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignBottom)

        self.retranslateUi(InfoManipulationDialog)
        self.buttonBox.accepted.connect(InfoManipulationDialog.accept)
        self.buttonBox.rejected.connect(InfoManipulationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InfoManipulationDialog)

    def retranslateUi(self, InfoManipulationDialog):
        _translate = QtCore.QCoreApplication.translate
        InfoManipulationDialog.setWindowTitle(_translate("InfoManipulationDialog", "Dialog"))


class InfoManipulationDialog(QDialog, Ui_InfoManipulationDialog):
    def __init__(
            self, window_title: str,
            widget_lines: Tuple[Tuple["QLabel", Union["QLineEdit", "QComboBox", "QSpinBox"]], ...],
            *args):
        super().__init__(*args)
        self.setupUi(self)
        self.setWindowTitle(window_title)
        self.widget_lines = widget_lines
        for line in self.widget_lines:
            self.optionLayout.addRow(*line)

    def get_widgets(self):
        return self.widget_lines


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QComboBox, QSpinBox

    app = QApplication(sys.argv)
    d = InfoManipulationDialog('321', ((QLabel('123'), QLineEdit()),))
    d.exec()
    print(d.get_widgets())
    sys.exit(0)
