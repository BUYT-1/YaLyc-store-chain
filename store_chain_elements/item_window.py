from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel

from .two_tab_window import TwoTabWindow


class ItemManagementWindow(TwoTabWindow):
    def __init__(self):
        super().__init__(
            main_add_meth=self.add_item, main_del_meth=self.delete_item,
            main_b3_meth=self.edit_item,
            sec_add_meth=self.add_supplier, sec_del_meth=self.delete_supplier,
            sec_b3_meth=self.edit_supplier,
            main_tab_name='Items', sec_tab_name='Suppliers',
            main_add_txt='Add item', main_del_txt='Delete item', main_b3_txt='Edit item',
            sec_add_txt='Add supplier', sec_del_txt='Delete supplier', sec_b3_txt='Edit supplier',
            main_headers=['ID', 'Name', 'Supplier'],
            sec_headers=['ID', 'Name']
        )
        self.update_tables()

    def update_tables(self):
        supplier_mapping = self.get_id_name_from_table('supplier')
        self.update_table(
            self.mainTable,
            ('ID', 'Name', 'Supplier'),
            'item',
            {
                'id': {},
                'name': {},
                'supplier_id': supplier_mapping
            }
        )

        self.update_table(
            self.secTable,
            ('ID', 'Name'),
            'supplier',
            {
                'id': {},
                'name': {}
            }
        )

    def add_item(self):
        supplier_box = QComboBox()
        mapping = self.index_map_boxes(((supplier_box, 'supplier'),))
        self.auto_add(
            "Enter info about the item",
            'item',
            ('name', 'supplier_id'),
            (QLineEdit(), supplier_box),
            ('Name', 'Supplier'),
            mapping
        )
        self.update_tables()

    def delete_item(self):
        ids = self.get_selected_ids(self.mainTable)
        self.db_del(
            'item',
            ids
        )
        self.update_tables()

    def edit_item(self):
        item_id = self.get_one_selected_id(self.mainTable)
        if item_id is None:
            self.statusBar().showMessage('Select 1 item', 1523)
            return
        supplier_box = QComboBox()
        mapping = self.index_map_boxes(((supplier_box, 'supplier'),))
        self.auto_edit(
            "Enter info about the item",
            'item',
            item_id,
            ('name', 'supplier_id'),
            (QLineEdit(), supplier_box),
            ('Name', 'Supplier'),
            mapping
        )
        self.update_tables()

    def add_supplier(self):
        self.auto_add(
            "Enter the supplier's name",
            'supplier',
            ('name',),
            (QLineEdit(),),
            ('Name',),
            {}
        )
        self.update_tables()

    def delete_supplier(self):
        ids = self.get_selected_ids(self.secTable)
        self.db_del(
            'supplier',
            ids
        )
        self.update_tables()

    def edit_supplier(self):
        supplier_id = self.get_one_selected_id(self.secTable)
        if supplier_id is None:
            self.statusBar().showMessage('Select 1 supplier', 1823)
            return
        supplier_box = QComboBox()
        mapping = self.index_map_boxes(((supplier_box, 'supplier'),))
        self.auto_edit(
            "Enter the supplier's new name",
            'supplier',
            supplier_id,
            ('name',),
            (QLineEdit(),),
            ('Name',),
            mapping
        )
        self.update_tables()
