from PyQt5.QtWidgets import QLineEdit, QComboBox, QSpinBox, QLabel

from .two_tab_window import TwoTabWindow


class EmployeeManagementWindow(TwoTabWindow):
    def __init__(self):
        super().__init__(
            main_add_meth=self.hire_employee, main_del_meth=self.fire_employee,
            main_b3_meth=self.edit_employee_info,
            sec_add_meth=self.add_position, sec_del_meth=self.delete_position,
            sec_b3_meth=self.change_position_info,
            main_tab_name='Employees', sec_tab_name='Positions',
            main_add_txt='Hire', main_del_txt='Fire', main_b3_txt='Edit info',
            sec_add_txt='Add position', sec_del_txt='Delete position', sec_b3_txt='Edit position',
            main_headers=['ID', 'Name', 'Shop', 'Position', 'Pay', 'Other info'],
            sec_headers=['ID', 'Name', 'Info']
        )
        self.update_tables()

    def update_tables(self):
        shop_mapping = self.get_id_name_from_table('shop')
        position_mapping = self.get_id_name_from_table('position')
        self.update_table(
            self.mainTable,
            ('ID', 'Name', 'Shop', 'Position', 'Salary', 'Other info'),
            'employee',
            {'id': {},
             'name': {},
             'shop_id': shop_mapping,
             'position_id': position_mapping,
             'salary': {},
             'other_info': {}
             }
        )
        self.update_table(
            self.secTable,
            ('ID', 'Name', 'Description'),
            'position',
            {
                'id': {},
                'name': {},
                'description': {}
            }
        )

    def hire_employee(self):
        shop_pick = QComboBox()
        position_pick = QComboBox()
        mapping = self.index_map_boxes(((shop_pick, 'shop'), (position_pick, 'position')))
        employee_spb = QSpinBox()
        employee_spb.setMaximum(2 ** 31 - 1)
        self.auto_add(
            "Enter employee's info",
            'employee',
            ('name', 'shop_id', 'position_id', 'salary', 'other_info'),
            (QLineEdit(), shop_pick, position_pick, employee_spb, QLineEdit()),
            ('Name', 'Shop', 'Position', 'Salary', 'Other info'),
            mapping
        )
        self.update_tables()

    def edit_employee_info(self):
        employee_id = self.get_one_selected_id(self.mainTable)
        if employee_id is None:
            self.statusBar().showMessage('Select 1 employee', 1234)
            return
        shop_pick = QComboBox()
        position_pick = QComboBox()
        mapping = self.index_map_boxes(((shop_pick, 'shop'), (position_pick, 'position')))
        employee_spb = QSpinBox()
        employee_spb.setMaximum(2 ** 31 - 1)
        self.auto_edit(
            'Edit employee info',
            'employee',
            employee_id,
            ('name', 'shop_id', 'position_id', 'salary', 'other_info'),
            (QLineEdit(), shop_pick, position_pick, employee_spb, QLineEdit()),
            ('Name', 'Shop', 'Position', 'Salary', 'Other info'),
            mapping
        )
        self.update_tables()

    def fire_employee(self):
        ids = self.get_selected_ids(self.mainTable)
        if not ids:
            self.statusBar().showMessage('Select 1 employee', 2133)
            return
        self.db_del(
            'employee',
            ids
        )
        self.update_tables()

    def add_position(self):
        self.auto_add(
            'Enter info about the position',
            'position',
            ('name', 'description'),
            (QLineEdit(), QLineEdit()),
            ('Name', 'Description'),
            {}
        )
        self.update_tables()

    def delete_position(self):
        ids = self.get_selected_ids(self.secTable)
        self.db_del(
            'position',
            ids
        )
        self.update_tables()

    def change_position_info(self):
        position_id = self.get_one_selected_id(self.secTable)
        if position_id is None:
            self.statusBar().showMessage('Select 1 position', 1957)
            return
        self.auto_edit(
            'Edit info about position',
            'position',
            position_id,
            ('Name', 'Description'),
            (QLineEdit(), QLineEdit()),
            ('Name', 'Description'),
            {}
        )
        self.update_tables()
