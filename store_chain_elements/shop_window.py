from functools import partial
from typing import Optional
import sqlite3

from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox, QSpinBox, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from .management_window import ManagementWindow
from .shop_widget import ShopWidget
from .info_manipulation_dialog import InfoManipulationDialog
from .values import STOCK_TR_TYPE, SELL_TR_TYPE


class Ui_ShopManagementWindow:
    def setupUi(self, ShopManagementWindow):
        ShopManagementWindow.setObjectName("ShopManagementWindow")
        ShopManagementWindow.resize(933, 600)
        self.centralwidget = QtWidgets.QWidget(ShopManagementWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Gentium Book Basic")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addShopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addShopBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.addShopBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.addShopBtn.setObjectName("addShopBtn")
        self.shopBtnGroup = QtWidgets.QButtonGroup(ShopManagementWindow)
        self.shopBtnGroup.setObjectName("shopBtnGroup")
        self.shopBtnGroup.addButton(self.addShopBtn)
        self.horizontalLayout.addWidget(self.addShopBtn)
        self.deleteShopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.deleteShopBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.deleteShopBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.deleteShopBtn.setObjectName("deleteShopBtn")
        self.shopBtnGroup.addButton(self.deleteShopBtn)
        self.horizontalLayout.addWidget(self.deleteShopBtn)
        self.editShopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.editShopBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.editShopBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.editShopBtn.setObjectName("editShopBtn")
        self.shopBtnGroup.addButton(self.editShopBtn)
        self.horizontalLayout.addWidget(self.editShopBtn)
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshBtn.sizePolicy().hasHeightForWidth())
        self.refreshBtn.setSizePolicy(sizePolicy)
        self.refreshBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.refreshBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.refreshBtn.setObjectName("refreshBtn")
        self.shopBtnGroup.addButton(self.refreshBtn)
        self.horizontalLayout.addWidget(self.refreshBtn)
        spacerItem = QtWidgets.QSpacerItem(154, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(300, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.widgetScroll = QtWidgets.QWidget()
        self.widgetScroll.setGeometry(QtCore.QRect(0, 0, 298, 498))
        self.widgetScroll.setObjectName("widgetScroll")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widgetScroll)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.shopLayout = QtWidgets.QVBoxLayout()
        self.shopLayout.setObjectName("shopLayout")
        self.verticalLayout_4.addLayout(self.shopLayout)
        self.scrollArea.setWidget(self.widgetScroll)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Gentium Book Basic")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addItemBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addItemBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.addItemBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.addItemBtn.setObjectName("addItemBtn")
        self.itemBtnGroup = QtWidgets.QButtonGroup(ShopManagementWindow)
        self.itemBtnGroup.setObjectName("itemBtnGroup")
        self.itemBtnGroup.addButton(self.addItemBtn)
        self.horizontalLayout_3.addWidget(self.addItemBtn)
        self.disposeOfItemBtn = QtWidgets.QPushButton(self.centralwidget)
        self.disposeOfItemBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.disposeOfItemBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.disposeOfItemBtn.setObjectName("disposeOfItemBtn")
        self.itemBtnGroup.addButton(self.disposeOfItemBtn)
        self.horizontalLayout_3.addWidget(self.disposeOfItemBtn)
        self.stockItemBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stockItemBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.stockItemBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.stockItemBtn.setObjectName("stockItemBtn")
        self.itemBtnGroup.addButton(self.stockItemBtn)
        self.horizontalLayout_3.addWidget(self.stockItemBtn)
        self.sellItemBtn = QtWidgets.QPushButton(self.centralwidget)
        self.sellItemBtn.setMinimumSize(QtCore.QSize(30, 28))
        self.sellItemBtn.setMaximumSize(QtCore.QSize(30, 28))
        self.sellItemBtn.setObjectName("sellItemBtn")
        self.itemBtnGroup.addButton(self.sellItemBtn)
        self.horizontalLayout_3.addWidget(self.sellItemBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.itemsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.itemsTable.setObjectName("itemsTable")
        self.itemsTable.setColumnCount(5)
        self.itemsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTable.setHorizontalHeaderItem(4, item)
        self.verticalLayout_2.addWidget(self.itemsTable)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        ShopManagementWindow.setCentralWidget(self.centralwidget)
        self.actionHow_to_use = QtWidgets.QAction(ShopManagementWindow)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionAbout = QtWidgets.QAction(ShopManagementWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(ShopManagementWindow)
        QtCore.QMetaObject.connectSlotsByName(ShopManagementWindow)

    def retranslateUi(self, ShopManagementWindow):
        _translate = QtCore.QCoreApplication.translate
        ShopManagementWindow.setWindowTitle(_translate("ShopManagementWindow", "Manage shops"))
        self.label.setText(_translate("ShopManagementWindow", "Shops"))
        self.addShopBtn.setText(_translate("ShopManagementWindow", "+"))
        self.deleteShopBtn.setText(_translate("ShopManagementWindow", "-"))
        self.editShopBtn.setText(_translate("ShopManagementWindow", "e"))
        self.refreshBtn.setText(_translate("ShopManagementWindow", "r"))
        self.label_2.setText(_translate("ShopManagementWindow", "Shop items"))
        self.addItemBtn.setText(_translate("ShopManagementWindow", "+"))
        self.disposeOfItemBtn.setText(_translate("ShopManagementWindow", "-"))
        self.stockItemBtn.setText(_translate("ShopManagementWindow", "↑"))
        self.sellItemBtn.setText(_translate("ShopManagementWindow", "↓"))
        item = self.itemsTable.horizontalHeaderItem(0)
        item.setText(_translate("ShopManagementWindow", "ID"))
        item = self.itemsTable.horizontalHeaderItem(1)
        item.setText(_translate("ShopManagementWindow", "Item"))
        item = self.itemsTable.horizontalHeaderItem(2)
        item.setText(_translate("ShopManagementWindow", "Shop"))
        item = self.itemsTable.horizontalHeaderItem(3)
        item.setText(_translate("ShopManagementWindow", "Price for one"))
        item = self.itemsTable.horizontalHeaderItem(4)
        item.setText(_translate("ShopManagementWindow", "Quantity available"))
        self.actionHow_to_use.setText(_translate("ShopManagementWindow", "How to use"))
        self.actionAbout.setText(_translate("ShopManagementWindow", "About..."))


class ShopManagementWindow(ManagementWindow, Ui_ShopManagementWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        for button, method in \
                (self.addShopBtn, self.add_shop), (self.deleteShopBtn, self.delete_shop), \
                (self.editShopBtn, self.edit_shop), (self.refreshBtn, self.update_data), \
                (self.addItemBtn, self.add_shop_item), \
                (self.disposeOfItemBtn, self.remove_shop_item), \
                (self.stockItemBtn, self.stock_item), (self.sellItemBtn, self.sell_item):
            button.clicked.connect(method)
        self.selected_shop_id: Optional[int] = None
        self.update_data()

    def update_data(self):
        data = self.connection.cursor().execute("""
        SELECT
            id, name
        FROM
            shop""").fetchall()

        # Clear the layout
        for i in reversed(range(self.shopLayout.count() - 1)):
            self.shopLayout.itemAt(i).widget().setParent(None)

        for shop_id, name in data:
            shop_widget = ShopWidget(shop_id)
            shop_widget.setText(str(name))
            shop_widget.clicked.connect(self.show_items_btn)
            self.shopLayout.addWidget(shop_widget)
        self.shopLayout.addSpacerItem(QtWidgets.QSpacerItem(
            1, 1, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding))
        if self.selected_shop_id is None:
            return
        self.show_shop_items(self.selected_shop_id)

    def show_shop_items(self, shop_id: int):
        self.selected_shop_id = shop_id
        items = self.get_id_name_from_table('item')
        shops = self.get_id_name_from_table('shop')
        self.update_table(
            self.itemsTable,
            ('ID', 'Item', 'Shop', 'Price for one', 'Quantity available'),
            'available_item',
            {
                'id': {},
                'item_id': items,
                'shop_id': shops,
                'price_one': {},
                'quantity': {}
            },
            condition=f'shop_id = {shop_id}'
        )

    def show_items_btn(self):
        shop_w: ShopWidget = self.sender()
        shop_id = shop_w.get_shop_id()
        self.show_shop_items(shop_id)

    def add_shop(self):
        self.auto_add(
            'Enter information about the shop',
            'shop',
            ('name',),
            (QLineEdit(),),
            ('Name',),
            {}
        )
        self.update_data()

    def delete_shop(self):
        shops_box = QComboBox()
        mapping = self.index_map_boxes(((shops_box, 'shop'),))
        dialog = InfoManipulationDialog(
            'Delete a shop',
            ((QLabel('Shop to delete'), shops_box),),
            self
        )
        confirmed = dialog.exec()
        if confirmed:
            shop_id = mapping[shops_box][shops_box.currentIndex()]
            self.db_del('shop', (shop_id,))
            self.update_data()

    def edit_shop(self):
        shops_box = QComboBox()
        mapping = self.index_map_boxes(((shops_box, 'shop'),))
        name_lbl = QLineEdit()
        dialog = InfoManipulationDialog(
            "Edit a shop's name",
            ((QLabel('Shop'), shops_box),
             (QLabel('Name'), name_lbl)),
            self
        )
        confirmed = dialog.exec()
        if confirmed:
            shop_id = mapping[shops_box][shops_box.currentIndex()]
            if shop_id is None:
                return
            self.db_edit('shop', shop_id, ('name',), (name_lbl.text(),))
            self.update_data()

    def add_shop_item(self):
        item_box = QComboBox()
        shop_box = QComboBox()
        mapping = self.index_map_boxes(((item_box, 'item'), (shop_box, 'shop')))
        price_spb = QSpinBox()
        price_spb.setMaximum(2 ** 31 - 1)
        quan_spb = QSpinBox()
        quan_spb.setMaximum(2 ** 31 - 1)
        self.auto_add(
            'Enter information about the item sold',
            'available_item',
            ('item_id', 'shop_id', 'price_one', 'quantity'),
            (item_box, shop_box, price_spb, quan_spb),
            ('Item', 'Shop', 'Price for one', 'Quantity'),
            mapping
        )
        self.update_data()

    def remove_shop_item(self):
        ids = self.get_selected_ids(self.itemsTable)
        if not ids:
            return
        self.db_del(
            'available_item',
            ids
        )
        self.update_data()

    def stock_item(self):
        item_id = self.get_one_selected_id(self.itemsTable)
        if item_id is None:
            self.statusBar().showMessage('Select 1 item', 1234)
            return
        quan_spb = QSpinBox()
        quan_spb.setMaximum(2 ** 31 - 1)
        money_spb = QSpinBox()
        money_spb.setMaximum(2 ** 31 - 1)
        dialog = InfoManipulationDialog(
            'Buying an item',
            (
                (QLabel('Quantity'), quan_spb),
                (QLabel('Money spent'), money_spb)
            ),
            self
        )
        confirmed = dialog.exec()
        if confirmed:
            cursor = self.connection.cursor()
            try:
                cursor.executescript(f"""
                UPDATE
                    available_item
                SET
                    quantity = quantity + {quan_spb.value()}
                WHERE
                    id = {item_id};
                INSERT INTO
                    [transaction](type, money_delta)
                VALUES
                    ({STOCK_TR_TYPE}, {-money_spb.value()})""")
                self.update_data()
            except sqlite3.IntegrityError:
                self.statusBar().showMessage('Wrong quantity', 5712)
            except sqlite3.Error as e:
                print(e)

    def sell_item(self):
        item_id = self.get_one_selected_id(self.itemsTable)
        if item_id is None:
            self.statusBar().showMessage('Select 1 item', 1632)
            return
        quan_spb = QSpinBox()
        quan_spb.setMaximum(2 ** 31 - 1)
        dialog = InfoManipulationDialog(
            'Selling an item',
            (
                (QLabel('Quantity'), quan_spb),
            ),
            self
        )
        conf = dialog.exec()
        if conf:
            cursor = self.connection.cursor()
            try:
                (price_one,) = cursor.execute(f"""
                SELECT 
                    price_one 
                FROM 
                    available_item 
                WHERE
                    id = {item_id}""").fetchone()
                cursor.executescript(f"""
                UPDATE
                    available_item
                SET
                    quantity = quantity - {quan_spb.value()}
                WHERE
                    id = {item_id};
                INSERT INTO
                    [transaction](type, money_delta)
                VALUES
                    ({SELL_TR_TYPE}, {quan_spb.value() * price_one})""")
                self.update_data()
            except sqlite3.IntegrityError:
                self.statusBar().showMessage('Wrong quantity', 5712)
            except sqlite3.Error as e:
                print(e)
