from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit

from src.utils.Signals import EventSignal

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.pixmap = QPixmap()

    def set_image_from_data(self, img):
        self.pixmap.loadFromData(img)
        self.pixmap = self.pixmap.scaled(128, 128, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)

    def set_image_from_file(self, path):
        self.pixmap.load(path)
        self.pixmap = self.pixmap.scaled(128, 128, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)

    def set_scale(self, x, y):
        self.pixmap = self.pixmap.scaled(x, y, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)

class ClickableImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.event_signal = EventSignal()

    def mousePressEvent(self, ev, QMouseEvent=None):
        self.event_signal.clicked.emit()


class ScrollableLabel(QLineEdit):
    def __init__(self, parent=None):
        super(ScrollableLabel, self).__init__(parent)

        self.setReadOnly(True)
        self.setStyleSheet("background-color:#00000000; font-size: 13px; border:0px")

