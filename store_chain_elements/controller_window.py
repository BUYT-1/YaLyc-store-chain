from functools import partial
from typing import Any, Dict
import sqlite3
import configparser

from .login_window import LoginWindow
from .selector_window import SelectorWindow
from .shop_window import ShopManagementWindow
from .employee_window import EmployeeManagementWindow
from .item_window import ItemManagementWindow
from .transaction_window import TransactionWindow
from .settings import Settings
from .functions import fix_config_file
from .values import DatabaseDoesntExist

# LANG_SETTING = -4609462400089563674  # Coming soon
DB_SETTING = 3969842491586116040


class Controller:
    def __init__(self):
        self.login_window = None
        self.selector_window = None
        self.other_window = None
        self.changed_settings: Dict[int, Any] = {
            DB_SETTING: None,
            # LANG_SETTING: None,
        }
        fix_config_file()

    def show_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.switch_to_selector.connect(self.show_selector_window)
        self.login_window.show()

    def show_selector_window(self):
        if self.login_window is not None:
            self.login_window.close()
            self.login_window = None
        if self.other_window is not None:
            self.other_window.close()
            self.other_window = None
        if self.selector_window is None:
            self.selector_window = SelectorWindow()
            w = self.selector_window
            for signal, method in \
                    (w.shops_selected,
                     partial(self.open_management_window, ShopManagementWindow)), \
                    (w.employees_selected,
                     partial(self.open_management_window, EmployeeManagementWindow)), \
                    (w.items_selected,
                     partial(self.open_management_window, ItemManagementWindow)), \
                    (w.transactions_selected,
                     partial(self.open_management_window, TransactionWindow)), \
                    (w.settings_selected, self.open_settings), \
                    (w.exit_selected, self.exit):
                signal.connect(method)
        self.selector_window.show()

    def open_management_window(self, window):
        if self.other_window is not None:
            self.other_window.close()
        try:
            self.other_window = window()
            self.other_window.closed.connect(self.show_selector_window)
            self.other_window.show()
        except sqlite3.Error:
            print('The database you are using is malformed.')
            print('Please select a different database using the Settings menu.')
            return
        except DatabaseDoesntExist:
            print('Please select a database file.')
            return
        if self.selector_window is not None:
            self.selector_window.hide()

    def open_settings(self):
        settings_dialog = Settings()

        settings_dialog.new_db_file_selected.connect(
            lambda info: self.changed_settings.__setitem__(DB_SETTING, info))

        changes_confirmed = settings_dialog.exec()
        if changes_confirmed:
            self.write_changes()
        for dict_key in self.changed_settings.keys():
            self.changed_settings[dict_key] = None

    def write_changes(self):
        fix_config_file()
        config = configparser.ConfigParser()
        config.read('configuration.cfg')
        for section, param, value in \
                (('Database', 'path_to_db', self.changed_settings[DB_SETTING]),):
            # ('Localization', 'language', self.changed_settings[LANG_SETTING]):
            if value is None:  # Setting didn't change
                continue
            config[section][param] = str(value)
        with open('configuration.cfg', 'w') as config_file:
            config.write(config_file)

    def exit(self):
        for window in self.login_window, self.selector_window, self.other_window:
            if window is not None:
                window.close()
        raise SystemExit

    # @staticmethod
    # def add_image_columns():
    #     with sqlite3.connect(get_db_path()) as connection:
    #         cursor = connection.cursor()
    #         for table_name in 'shop', 'supplier', 'item', 'employee':
    #             try:
    #                 cursor.execute(
    #                     f"""ALTER TABLE [{table_name}] ADD COLUMN path_to_image STRING""")
    #             except sqlite3.Error as e:
    #                 print(e)
    #         connection.commit()
