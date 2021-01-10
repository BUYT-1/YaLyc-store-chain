import os
from secrets import token_hex

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets

from .functions import check_password, hash_data


class Ui_loginWidget:
    def setupUi(self, loginWidget):
        loginWidget.setObjectName("loginWidget")
        loginWidget.resize(267, 165)
        loginWidget.setMinimumSize(QtCore.QSize(220, 150))
        loginWidget.setMaximumSize(QtCore.QSize(354, 185))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(loginWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.usernameLine = QtWidgets.QLineEdit(loginWidget)
        self.usernameLine.setAlignment(QtCore.Qt.AlignCenter)
        self.usernameLine.setObjectName("usernameLine")
        self.verticalLayout_2.addWidget(self.usernameLine)
        self.passwordLine = QtWidgets.QLineEdit(loginWidget)
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLine.setObjectName("passwordLine")
        self.verticalLayout_2.addWidget(self.passwordLine)
        self.loginBtn = QtWidgets.QPushButton(loginWidget)
        self.loginBtn.setObjectName("loginBtn")
        self.verticalLayout_2.addWidget(self.loginBtn, 0, QtCore.Qt.AlignHCenter)
        self.msgLbl = QtWidgets.QLabel(loginWidget)
        self.msgLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.msgLbl.setObjectName("msgLbl")
        self.verticalLayout_2.addWidget(self.msgLbl)

        self.retranslateUi(loginWidget)
        QtCore.QMetaObject.connectSlotsByName(loginWidget)

    def retranslateUi(self, loginWidget):
        _translate = QtCore.QCoreApplication.translate
        loginWidget.setWindowTitle(_translate("loginWidget", "Log in"))
        self.usernameLine.setPlaceholderText(_translate("loginWidget", "Username"))
        self.passwordLine.setPlaceholderText(_translate("loginWidget", "Password"))
        self.loginBtn.setText(_translate("loginWidget", "Login"))
        self.msgLbl.setText(_translate("loginWidget", "Enter your username and password"))


class LoginWindow(QWidget, Ui_loginWidget):
    switch_to_selector = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginBtn.clicked.connect(self.check_login)
        self.loginBtn.setText('Login' if self.is_registered() else 'Register')

    def check_login(self):
        if not self.is_registered():
            self.register()
        else:
            self.login()

    def is_registered(self):
        return os.path.isfile('credentials.txt')

    def register(self):
        username_input = self.usernameLine.text()
        password_input = self.passwordLine.text()
        if not check_password(password_input):
            self.msgLbl.setText('Weak password')
            return
        try:
            with open('credentials.txt', 'w') as credentials_file:
                print(username_input, file=credentials_file)
                salt = token_hex()
                print(hash_data(password_input, salt), file=credentials_file)
                print(salt, file=credentials_file)
            self.switch_to_selector.emit()
        except OSError:
            self.msgLbl.setText('Error when registering')
            return

    def login(self):
        username_input = self.usernameLine.text()
        password_input = self.passwordLine.text()
        try:
            with open('credentials.txt', 'r') as credentials_file:
                # [:-1] to strip the newline character
                username = credentials_file.readline()[:-1]
                pass_hash = credentials_file.readline()[:-1]
                salt = credentials_file.readline()[:-1]
        except OSError:
            self.msgLbl.setText('Error when accessing the login credentials file')
            return
        if hash_data(password_input, salt) == pass_hash \
                and username_input == username:
            self.switch_to_selector.emit()
        else:
            self.msgLbl.setText('Wrong username or password')
