import sqlite3

from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets

from .functions import get_db_path
from .values import TABLES


class Ui_WindowSelector(object):
    def setupUi(self, WindowSelector):
        WindowSelector.setObjectName("WindowSelector")
        WindowSelector.resize(355, 271)
        WindowSelector.setMinimumSize(QtCore.QSize(310, 250))
        WindowSelector.setMaximumSize(QtCore.QSize(400, 340))
        self.centralwidget = QtWidgets.QWidget(WindowSelector)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.manageShopsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.manageShopsBtn.setObjectName("manageShopsBtn")
        self.verticalLayout_2.addWidget(self.manageShopsBtn)
        self.manageEmployeesBtn = QtWidgets.QPushButton(self.centralwidget)
        self.manageEmployeesBtn.setObjectName("manageEmployeesBtn")
        self.verticalLayout_2.addWidget(self.manageEmployeesBtn)
        self.manageItemsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.manageItemsBtn.setObjectName("manageItemsBtn")
        self.verticalLayout_2.addWidget(self.manageItemsBtn)
        self.manageTransactionsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.manageTransactionsBtn.setObjectName("manageTransactionsBtn")
        self.verticalLayout_2.addWidget(self.manageTransactionsBtn)
        self.settingsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.settingsBtn.setObjectName("settingsBtn")
        self.verticalLayout_2.addWidget(self.settingsBtn)
        self.checkDbIntegrityBtn = QtWidgets.QPushButton(self.centralwidget)
        self.checkDbIntegrityBtn.setObjectName("checkDbIntegrityBtn")
        self.verticalLayout_2.addWidget(self.checkDbIntegrityBtn)
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitBtn.setObjectName("exitBtn")
        self.verticalLayout_2.addWidget(self.exitBtn)
        WindowSelector.setCentralWidget(self.centralwidget)

        self.retranslateUi(WindowSelector)
        QtCore.QMetaObject.connectSlotsByName(WindowSelector)

    def retranslateUi(self, WindowSelector):
        _translate = QtCore.QCoreApplication.translate
        WindowSelector.setWindowTitle(_translate("WindowSelector", "Select an option"))
        self.manageShopsBtn.setText(_translate("WindowSelector", "Manage shops"))
        self.manageEmployeesBtn.setText(_translate("WindowSelector", "Manage employees"))
        self.manageItemsBtn.setText(_translate("WindowSelector", "Manage items"))
        self.manageTransactionsBtn.setText(_translate("WindowSelector", "Manage transactions"))
        self.settingsBtn.setText(_translate("WindowSelector", "Settings"))
        self.checkDbIntegrityBtn.setText(_translate("WindowSelector", "Check DB integrity"))
        self.exitBtn.setText(_translate("WindowSelector", "Exit"))


class SelectorWindow(QMainWindow, Ui_WindowSelector):
    shops_selected = pyqtSignal()
    employees_selected = pyqtSignal()
    items_selected = pyqtSignal()
    transactions_selected = pyqtSignal()
    settings_selected = pyqtSignal()
    exit_selected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        for button, signal in (self.manageShopsBtn, self.shops_selected), \
                              (self.manageEmployeesBtn, self.employees_selected), \
                              (self.manageItemsBtn, self.items_selected), \
                              (self.manageTransactionsBtn, self.transactions_selected), \
                              (self.settingsBtn, self.settings_selected), \
                              (self.exitBtn, self.exit_selected):
            button.clicked.connect(signal.emit)
        self.checkDbIntegrityBtn.clicked.connect(self.db_integrity_check)

    def db_integrity_check(self):
        bad_tables = self.get_malformed_tables()
        if bad_tables:
            error_msg_dialog = QErrorMessage()
            error_msg_dialog.showMessage(
                f'Integrity check failed. Malformed tables: {", ".join(bad_tables)}')
            error_msg_dialog.exec()
        else:
            self.statusBar().showMessage('Integrity check passed.', 5000)

    @staticmethod
    def get_malformed_tables() -> list:
        bad_tables = []
        path = get_db_path()
        if path is None:
            print('Database file does not exist or is not selected.')
            return list(TABLES.keys())
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            for table_name, column_names in TABLES.items():
                try:
                    cursor.execute(
                        f"""SELECT {', '.join(column_names)} FROM [{table_name}]""")
                except sqlite3.Error as e:
                    print('Error:', e)
                    bad_tables.append(table_name)
        return bad_tables
