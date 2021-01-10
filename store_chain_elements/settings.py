import configparser

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets

from .functions import fix_config_file
from .shared_constants import HOME_DIR


class Ui_Settings:
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(390, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(30, 60, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dbChooseBtn = QtWidgets.QPushButton(Settings)
        self.dbChooseBtn.setGeometry(QtCore.QRect(30, 20, 141, 28))
        self.dbChooseBtn.setObjectName("dbChooseBtn")

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.dbChooseBtn.setText(_translate("Settings", "Choose database file"))


class Settings(QDialog, Ui_Settings):
    # new_language_selected = pyqtSignal(str)
    new_db_file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(390, 100)
        self.connect_signals()
        self.load_from_config()

    def connect_signals(self):
        for signal_qt, signal_class in ((self.dbChooseBtn.clicked, self.db_file_select),):
            # Language selection coming soon
            signal_qt.connect(signal_class)

    def load_from_config(self):
        fix_config_file()
        config = configparser.ConfigParser()
        config.read('configuration.cfg')
        # More coming soon
        # self.languageComboBox.setCurrentText(config['Localization']['language'])

    def db_file_select(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Choose the database', HOME_DIR, 'All files (*)')[0]
        if filename != filename.rstrip():
            # configparser lib messes it up, so that had to be forbidden
            print('The filename of your database has to have no spaces at its end.')
            return
        if filename:
            self.new_db_file_selected.emit(filename)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    sys.exit(Settings().exec())
