from PyQt5.QtWidgets import *
from src.views.components.SpecialLabels import  *
from src.utils.Signals import *

import logging

logger = logging.getLogger(__name__)

class MusicEntry(QWidget):
    IMAGE_DATA = 0
    IMAGE_PATH = 1
    def __init__(self, id, name, artist, mode, img, parent=None):
        super().__init__(parent)

        self.id = id
        self.name = name
        self.artist = artist

        if len(self.name)>50:
            self.name = self.name[:50] + "..."

        self.img_label = ImageLabel()
        self.update_image(mode, img)

        self.event_signal = EventSignal()

        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.view = QHBoxLayout()

        self.music_info = QVBoxLayout()
        self.music_info.setSpacing(0)

        self.title_label = QLabel(self.name)
        self.title_label.setStyleSheet("font-weight: bold; font-size:14px")

        self.artist_label = QLabel(self.artist)

        self.music_info.addWidget(self.title_label)
        self.music_info.addWidget(self.artist_label)
        self.music_info.setAlignment(Qt.AlignVCenter)

        self.view.addWidget(self.img_label)
        self.view.addLayout(self.music_info)
        self.view.addStretch()

        self.setLayout(self.view)

    def set_highlight(self):
        self.setStyleSheet("background-color: lightblue")

    def clear_highlight(self):
        self.setStyleSheet("")

    def update_image(self, mode, img):
        if mode == self.IMAGE_DATA:
            self.img_label.set_image_from_data(img)
        elif mode == self.IMAGE_PATH:
            self.img_label.set_image_from_file(img)
        self.img_label.set_scale(48, 48)

    def update_all(self, name, artist, mode, img): # TODO: BUGGY - NO TITLE SHORTENING
        self.title_label.setText(name)
        self.artist_label.setText(artist)
        self.update_image(mode, img)

    def mousePressEvent(self, ev, QMouseEvent=None):
        self.event_signal.clicked.emit(self.id)
        
class MusicEntryGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.collection = {}
        self.prev = None
        self.current = None

    def __contains__(self, item):
        if item in self.collection.keys():
            return True
        else:
            return False

    def add(self, id, obj):
        logger.debug(id)
        self.collection[id] = obj
        obj.event_signal.clicked.connect(self.on_entry_click)

    def get(self, id):
        return self.collection[id]

    def on_entry_click(self, id):
        self.prev = self.current
        self.current = self.collection[id]

        self.current.set_highlight()
        if self.prev is not None and self.prev != self.current:
            self.prev.clear_highlight()


