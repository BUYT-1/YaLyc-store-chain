from typing import Callable

from PyQt5 import QtCore, QtWidgets

from .management_window import ManagementWindow


class Ui_TwoTabWindow:
    def setupUi(self, TwoTabWindow):
        TwoTabWindow.setObjectName("TwoTabWindow")
        TwoTabWindow.resize(800, 604)
        TwoTabWindow.setWindowTitle("")
        self.centralwidget = QtWidgets.QWidget(TwoTabWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainBtnLayout = QtWidgets.QHBoxLayout()
        self.mainBtnLayout.setObjectName("mainBtnLayout")
        self.mainAddBtn = QtWidgets.QPushButton(self.mainTab)
        self.mainAddBtn.setObjectName("mainAddBtn")
        self.mainBtnLayout.addWidget(self.mainAddBtn)
        self.mainDelBtn = QtWidgets.QPushButton(self.mainTab)
        self.mainDelBtn.setObjectName("mainDelBtn")
        self.mainBtnLayout.addWidget(self.mainDelBtn)
        self.mainBtn3 = QtWidgets.QPushButton(self.mainTab)
        self.mainBtn3.setObjectName("mainBtn3")
        self.mainBtnLayout.addWidget(self.mainBtn3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainBtnLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.mainBtnLayout)
        self.mainTable = QtWidgets.QTableWidget(self.mainTab)
        self.mainTable.setObjectName("mainTable")
        self.mainTable.setColumnCount(0)
        self.mainTable.setRowCount(0)
        self.verticalLayout.addWidget(self.mainTable)
        self.tabWidget.addTab(self.mainTab, "")
        self.secTab = QtWidgets.QWidget()
        self.secTab.setObjectName("secTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.secTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.secBtnLayout = QtWidgets.QHBoxLayout()
        self.secBtnLayout.setObjectName("secBtnLayout")
        self.secAddBtn = QtWidgets.QPushButton(self.secTab)
        self.secAddBtn.setObjectName("secAddBtn")
        self.secBtnLayout.addWidget(self.secAddBtn)
        self.secDelBtn = QtWidgets.QPushButton(self.secTab)
        self.secDelBtn.setObjectName("secDelBtn")
        self.secBtnLayout.addWidget(self.secDelBtn)
        self.secBtn3 = QtWidgets.QPushButton(self.secTab)
        self.secBtn3.setObjectName("secBtn3")
        self.secBtnLayout.addWidget(self.secBtn3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.secBtnLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.secBtnLayout)
        self.secTable = QtWidgets.QTableWidget(self.secTab)
        self.secTable.setObjectName("secTable")
        self.secTable.setColumnCount(0)
        self.secTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.secTable)
        self.tabWidget.addTab(self.secTab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        TwoTabWindow.setCentralWidget(self.centralwidget)
        self.actionHow_to_use = QtWidgets.QAction(TwoTabWindow)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionAbout = QtWidgets.QAction(TwoTabWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(TwoTabWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TwoTabWindow)

    def retranslateUi(self, TwoTabWindow):
        _translate = QtCore.QCoreApplication.translate
        self.mainAddBtn.setText(_translate("TwoTabWindow", "Add"))
        self.mainDelBtn.setText(_translate("TwoTabWindow", "Delete"))
        self.mainBtn3.setText(_translate("TwoTabWindow", "Edit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), _translate("TwoTabWindow", "Tab 1"))
        self.secAddBtn.setText(_translate("TwoTabWindow", "Add"))
        self.secDelBtn.setText(_translate("TwoTabWindow", "Delete"))
        self.secBtn3.setText(_translate("TwoTabWindow", "Edit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.secTab), _translate("TwoTabWindow", "Tab 2"))
        self.actionHow_to_use.setText(_translate("TwoTabWindow", "How to use"))
        self.actionAbout.setText(_translate("TwoTabWindow", "About..."))


class TwoTabWindow(ManagementWindow, Ui_TwoTabWindow):
    """A generic two tab and table, three button each, window constructor.

    A class which constructs windows using the given parameters. The windows
    constructed have the following structure: a QTabWidget with two tabs, each
    consisting of three QPushButtons and a QTableWidget. These windows are
    designed to work with the SQLite DB used in the program."""

    def __init__(self, *,
                 main_add_meth: Callable, main_del_meth: Callable, main_b3_meth: Callable,
                 sec_add_meth: Callable, sec_del_meth: Callable, sec_b3_meth: Callable,
                 main_tab_name='Tab 1', sec_tab_name='Tab 2',
                 main_add_txt='Add', main_del_txt='Delete', main_b3_txt='Edit',
                 sec_add_txt='Add', sec_del_txt='Delete', sec_b3_txt='Edit',
                 main_headers: list = None, sec_headers: list = None):
        super().__init__()
        self.setupUi(self)
        for headers, table in (main_headers, self.mainTable), (sec_headers, self.secTable):
            headers = headers or []
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
        for button, text in (self.mainAddBtn, main_add_txt), (self.mainDelBtn, main_del_txt),\
                            (self.secAddBtn, sec_add_txt), (self.secDelBtn, sec_del_txt),\
                            (self.mainBtn3, main_b3_txt), (self.secBtn3, sec_b3_txt):
            button.setText(text)
        for button, method in \
                (self.mainAddBtn, main_add_meth), (self.mainDelBtn, main_del_meth),\
                (self.mainBtn3, main_b3_meth), (self.secAddBtn, sec_add_meth),\
                (self.secDelBtn, sec_del_meth), (self.secBtn3, sec_b3_meth):
            button.clicked.connect(method)
        self.tabWidget.setTabText(0, main_tab_name)
        self.tabWidget.setTabText(1, sec_tab_name)
