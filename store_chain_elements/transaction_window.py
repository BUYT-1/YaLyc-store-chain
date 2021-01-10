from PyQt5.QtWidgets import QComboBox, QSpinBox, QLabel
from PyQt5 import QtCore, QtWidgets

from .management_window import ManagementWindow
from .info_manipulation_dialog import InfoManipulationDialog
from .values import EARN_TR_TYPE, SPEND_TR_TYPE, SELL_TR_TYPE, STOCK_TR_TYPE


class Ui_TransactionWindow:
    def setupUi(self, TransactionWindow):
        TransactionWindow.setObjectName("TransactionWindow")
        TransactionWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(TransactionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addTransactionBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addTransactionBtn.setObjectName("addTransactionBtn")
        self.horizontalLayout.addWidget(self.addTransactionBtn)
        self.deleteTransactionBtn = QtWidgets.QPushButton(self.centralwidget)
        self.deleteTransactionBtn.setObjectName("deleteTransactionBtn")
        self.horizontalLayout.addWidget(self.deleteTransactionBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.transactionTable = QtWidgets.QTableWidget(self.centralwidget)
        self.transactionTable.setObjectName("transactionTable")
        self.transactionTable.setColumnCount(3)
        self.transactionTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.transactionTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transactionTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transactionTable.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.transactionTable)
        TransactionWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TransactionWindow)
        QtCore.QMetaObject.connectSlotsByName(TransactionWindow)

    def retranslateUi(self, TransactionWindow):
        _translate = QtCore.QCoreApplication.translate
        TransactionWindow.setWindowTitle(_translate("TransactionWindow", "Manage transactions"))
        self.addTransactionBtn.setText(_translate("TransactionWindow", "Add"))
        self.deleteTransactionBtn.setText(_translate("TransactionWindow", "Remove last"))
        item = self.transactionTable.horizontalHeaderItem(0)
        item.setText(_translate("TransactionWindow", "ID"))
        item = self.transactionTable.horizontalHeaderItem(1)
        item.setText(_translate("TransactionWindow", "Type"))
        item = self.transactionTable.horizontalHeaderItem(2)
        item.setText(_translate("TransactionWindow", "Money change"))


class TransactionWindow(ManagementWindow, Ui_TransactionWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.addTransactionBtn.clicked.connect(self.add_transaction)
        self.deleteTransactionBtn.clicked.connect(self.delete_last_transactions)
        self.update_transaction_table()

    def update_transaction_table(self):
        self.update_table(
            self.transactionTable,
            ('ID', 'Type', 'Change in money'),
            'transaction',
            {'id': {},
             'type':
                 {str(EARN_TR_TYPE): 'Earned money',
                  str(SPEND_TR_TYPE): 'Spent money',
                  str(SELL_TR_TYPE): 'Items sold',
                  str(STOCK_TR_TYPE): 'Items stocked'},
             'money_delta': {}}
        )

    def add_transaction(self):
        type_box = QComboBox()
        type_box.addItem('Earned')
        type_box.addItem('Spent')
        money_delta_sp_box = QSpinBox()
        money_delta_sp_box.setMaximum(2 ** 31 - 1)
        dialog = InfoManipulationDialog(
            'Add a transaction',
            (
                (QLabel('Type'), type_box),
                (QLabel('Money amount'), money_delta_sp_box)
            ),
            self
        )
        confirmed = dialog.exec()
        if confirmed:
            is_earned = type_box.currentText() == 'Earned'
            self.db_add(
                'transaction',
                ('type', 'money_delta'),
                (EARN_TR_TYPE if is_earned else SPEND_TR_TYPE,
                 money_delta_sp_box.value() * (is_earned * 2 - 1))
            )
            self.connection.commit()
            self.update_transaction_table()

    def delete_last_transactions(self):
        tr_num_box = QSpinBox()
        tr_num_box.setMaximum(2 ** 31 - 1)
        dialog = InfoManipulationDialog(
            'Delete X last transactions',
            ((QLabel('Remove x last transactions'), tr_num_box),)
        )
        confirmed = dialog.exec()
        if confirmed:
            self.connection.cursor().execute(f"""
            DELETE FROM
                [transaction]
            ORDER BY
                id DESC
            LIMIT 
                {tr_num_box.value()}""")
            self.connection.commit()
            self.update_transaction_table()
