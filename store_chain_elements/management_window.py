import sqlite3
from typing import Tuple, Union, Dict, Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import \
    (QMainWindow, QLabel, QLineEdit, QComboBox, QSpinBox, QTableWidget,
     QTableWidgetItem)

from .functions import get_db_path, get_info
from .info_manipulation_dialog import InfoManipulationDialog
from .values import DatabaseDoesntExist


class ManagementWindow(QMainWindow):
    """A base management window."""

    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        path = get_db_path()
        if path is None:
            raise DatabaseDoesntExist
        self.connection = sqlite3.connect(path)

    def update_table(self, table: QTableWidget, headers: Tuple[str, ...],
                     sql_table_name: str,
                     column_info: Dict[str, Dict[str, str]],
                     condition=1):
        table.setHorizontalHeaderLabels(headers)
        table.setColumnCount(len(headers))
        query = f"""
        SELECT
            {','.join(name for name in column_info.keys())}
        FROM
            [{sql_table_name}]
        WHERE
            {condition}
        """
        try:
            cursor = self.connection.cursor()
            data = cursor.execute(query).fetchall()
            table.setRowCount(0)
            for row_num, row in enumerate(data):
                table.setRowCount(table.rowCount() + 1)
                for col_num, (elem, translation) in enumerate(zip(row, column_info.values())):
                    elem = str(elem)
                    table.setItem(
                        row_num, col_num, QTableWidgetItem(translation.get(elem, elem)))
        except sqlite3.Error as e:
            print(query)
            print(e)
        table.resizeColumnsToContents()

    def get_id_name_from_table(self, table_name: str) -> Dict[str, str]:
        try:
            cursor = self.connection.cursor()
            return {str(row_id): str(name) for row_id, name in
                    cursor.execute(f'SELECT id, name FROM [{table_name}]').fetchall()}
        except sqlite3.Error as e:
            print(table_name)
            print(e)

    def db_exec(self, query: str, values: Tuple[Union[str, int], ...]):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.Error as e:
            print(query)
            print(values)
            print(e)

    def db_del(self, table_name: str, ids: Tuple[int, ...]):
        query = f"""
        DELETE FROM
            [{table_name}]
        WHERE
            id in ({','.join('?' for _ in ids)})"""
        self.db_exec(query, ids)

    def db_edit(self, table_name: str, row_id: int, columns: Tuple[str, ...],
                values: Tuple[str, ...]):
        query = f"""
            UPDATE
                [{table_name}]
            SET
                {', '.join(f"{column} = ?" for column in columns)}
            WHERE
                id = ?
        """
        self.db_exec(query, values + (row_id,))

    def db_add(self, table_name: str, columns: Tuple[str, ...], values: Tuple[str, ...]):
        query = f"""
            INSERT INTO
                [{table_name}]({','.join(columns)})
            VALUES
                ({','.join('?' for _ in columns)})"""
        self.db_exec(query, values)

    def index_map_boxes(
            self, box_table: Tuple[Tuple[QComboBox, str], ...]
    ) -> Dict[QComboBox, Dict[int, Optional[int]]]:
        """Add names to boxes and map their indexes to database IDs.

        Fill QComboBoxes with names from tables given and map the indexes of
        their items to database IDs and put a null item as the first one,
        then return the dict with the mapping."""
        mapping = {box: {0: None} for (box, _) in box_table}
        for box, table in box_table:
            data = self.get_id_name_from_table(table)
            box.addItem('')
            for i, (row_id, name) in enumerate(data.items(), start=1):
                box.addItem(str(name))
                mapping[box][i] = row_id
        return mapping

    def get_info_row(self, window_title: str,
                     widgets: Tuple[Union[QLineEdit, QComboBox, QSpinBox], ...],
                     label_texts: Tuple[str, ...]) -> InfoManipulationDialog:

        dialog = InfoManipulationDialog(
            window_title,
            tuple((QLabel(label_text), widget)
                  for label_text, widget in zip(label_texts, widgets)),
            self
        )
        confirmed = dialog.exec()
        return dialog if confirmed else None

    def auto_add(self, window_title: str, table_name: str,
                 column_names: Tuple[str, ...],
                 widgets: Tuple[Union[QLineEdit, QComboBox, QSpinBox], ...],
                 label_texts: Tuple[str, ...],
                 index_mapping: Dict[QComboBox, Dict[int, Optional[int]]]
                 ):
        dialog = self.get_info_row(window_title, widgets, label_texts)
        if dialog is not None:
            self.db_add(
                table_name,
                column_names,
                tuple(get_info(widget, index_mapping) for widget in widgets)
            )

    def auto_edit(self, window_title: str, table_name: str, row_id: int,
                  column_names: Tuple[str, ...],
                  widgets: Tuple[Union[QLineEdit, QComboBox, QSpinBox], ...],
                  label_texts: Tuple[str, ...],
                  index_mapping: Dict[QComboBox, Dict[int, Optional[int]]]
                  ):
        dialog = self.get_info_row(window_title, widgets, label_texts)
        if dialog is not None:
            self.db_edit(
                table_name,
                row_id,
                column_names,
                tuple(get_info(widg, index_mapping) for widg in widgets)
            )

    @staticmethod
    def get_selected_ids(table: QTableWidget) -> tuple:
        rows = {item.row() for item in table.selectedItems()}
        ids = tuple(table.item(row, 0).text() for row in rows)
        return ids

    def get_one_selected_id(self, table: QTableWidget) -> Optional[int]:
        ids = self.get_selected_ids(table)
        if len(ids) != 1:
            return None
        return ids[0]

    def closeEvent(self, event) -> None:
        self.connection.close()
        self.closed.emit()
        super().closeEvent(event)
