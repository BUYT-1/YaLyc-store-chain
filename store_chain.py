import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from store_chain_elements.controller_window import Controller


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 4K people...
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_login_window()
    sys.excepthook = except_hook
    sys.exit(app.exec())
