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
            super().__init__(*args, **kwargs)

        # QPushButton doesn't have a .setWordWrap method, but QLabel does, which
        # is what is used here
        self._label = QLabel(self)
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # Just like on a QPushButton

        # Disabling this makes resizing smoother
        self._label.setMouseTracking(False)
        self._label.setTextInteractionFlags(Qt.NoTextInteraction)

        # Make the text a bit prettier
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

    def __init__(self, shop_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = QHBoxLayout(self)
        self._button = QLabeledPushButton(self)
        self._button.clicked.connect(self.clicked.emit)
        self._icon = None
        self._id = shop_id
        self.initUi()

    def initUi(self):
        self._button.setFixedHeight(HEIGHT)
        self._layout.addWidget(self._button)
        self._button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

    def setText(self, text: str):
        self._button.setText(text)

    def set_icon(self, pixmap: QPixmap):
        icon = QLabel()
        resized_pixmap = pixmap.scaled(HEIGHT, HEIGHT, Qt.KeepAspectRatio)
        icon.setPixmap(resized_pixmap)
        if self._icon is not None:
            self._layout.removeWidget(self._icon)
        self._icon = icon
        self._layout.addWidget(self._icon)

    def get_shop_id(self):
        return self._id


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = ShopWidget(11)
    widget.setText('Shop at When Street')
    widget.resize(1000, 70)
    # widget.set_icon(QPixmap('../icons/test_icon.jpeg'))
    widget.clicked.connect(lambda: print(123))
    widget.show()
    sys.exit(app.exec())
