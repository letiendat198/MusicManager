from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit

from src.utils.Signals import EventSignal

class ImageLabel(QLabel):
    def __init__(self):
        super(ImageLabel, self).__init__()
        self.pixmap = QPixmap()
        self.signal = EventSignal()

    def mousePressEvent(self, ev, QMouseEvent=None):
        self.signal.clicked.emit()

    def set_image_from_data(self, img):
        self.pixmap.loadFromData(img)
        self.pixmap = self.pixmap.scaled(128, 128, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)

    def set_image_from_file(self, path):
        self.pixmap.load(path)
        self.pixmap = self.pixmap.scaled(128, 128, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)


class ScrollableLabel(QLineEdit):
    def __init__(self):
        super(ScrollableLabel, self).__init__()

        self.setReadOnly(True)
        self.setStyleSheet("background-color:#00000000; font-size: 13px; border:0px")

