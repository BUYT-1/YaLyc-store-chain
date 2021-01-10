from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap

HEIGHT = 40
LABEL_OFFSET = 4  # Making the text on the button look nicer


class QLabeledPushButton(QPushButton):
    """QPushButton with text wrapping."""

    def __init__(self, *args, **kwargs):
        if len(args) in (2, 3):
            *icon, text, parent = args
            super().__init__(*icon, '', parent)
        else:
            text = None
            super().__init__(*args)

        # QPushButton doesn't have a .setWordWrap method, but QLabel does, which
        # is what is used here
        self._label = QLabel(self)
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Disabling this makes resizing smoother
        self._label.setTextInteractionFlags(Qt.NoTextInteraction)
        self._label.setMouseTracking(False)

        self._label.setGeometry(
            LABEL_OFFSET, 0, self.width() - LABEL_OFFSET, self.height() - LABEL_OFFSET)

        # Reusability, just in case something else wants to use it
        if text is not None:
            self.setText(text)

    def setText(self, text: str):
        self._label.setText(text)

    def text(self) -> str:
        return self._label.text()

    def resizeEvent(self, event) -> None:
        self._label.setGeometry(
            LABEL_OFFSET, 0, self.width() - LABEL_OFFSET, self.height() - LABEL_OFFSET)


class ShopWidget(QWidget):
    """Shop selection widget.

    A compound widget which consists of a QLabel showing the net income
    of the shop, a clickable button with its name and a QLabel with the QPixmap
    icon of the shop.
    The button is a subclass of QPushButton which has the ability to wrap text.
    """

    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = QHBoxLayout(self)
        self._money_label = QLabel('0', self)
        self._money_label.setStyleSheet('QLabel {color: grey}')
        self._money_label.setMaximumWidth(self._money_label.sizeHint().width())
        self._button = QLabeledPushButton(self)
        self._button.clicked.connect(self.clicked.emit)
        self._icon = None
        self.initUi()

    def initUi(self):
        self._button.setFixedHeight(HEIGHT)
        self._money_label.setFixedHeight(HEIGHT)
        self._layout.addWidget(self._money_label)
        self._layout.addWidget(self._button)
        self._button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

    def setText(self, text: str):
        self._button.setText(text)

    def set_money(self, money: int):
        if not isinstance(money, int):
            raise TypeError(f'Expected type: int, got: {type(money).__name__}')
        self._money_label.setText(f'{money:+}')
        self._money_label.setMaximumWidth(self._money_label.sizeHint().width())
        if money < 0:
            self._money_label.setStyleSheet('QLabel {color: red}')
        elif money > 0:
            self._money_label.setStyleSheet('QLabel {color: green}')
        else:
            self._money_label.setStyleSheet('QLabel {color: grey}')

    def set_icon(self, pixmap: QPixmap):
        icon = QLabel()
        resized_pixmap = pixmap.scaled(HEIGHT, HEIGHT, Qt.KeepAspectRatio)
        icon.setPixmap(resized_pixmap)
        if self._icon is not None:
            self._layout.removeWidget(self._icon)
        self._icon = icon
        self._layout.addWidget(self._icon)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = ShopWidget()
    widget.setText('Shop at When Street')
    widget.set_money(+1241)
    widget.resize(1000, 70)
    widget.set_icon(QPixmap('../icons/test_icon.jpeg'))
    widget.clicked.connect(lambda: print(123))
    widget.show()
    sys.exit(app.exec())
