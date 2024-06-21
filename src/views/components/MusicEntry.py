from PyQt5.QtWidgets import *
from src.views.components.SpecialLabels import  *
from src.utils.Signals import *

import logging

logger = logging.getLogger(__name__)

class MusicEntry(QWidget):
    def __init__(self, id, name, img_data, artist):
        super().__init__()

        self.id = id
        self.name = name
        self.artist = artist

        self.img_label = ImageLabel()
        if img_data is not None: self.img_label.set_image_from_data(img_data)

        self.signal = EventSignal()

        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.view = QHBoxLayout()

        self.view.addWidget(self.img_label)

        self.music_info = QVBoxLayout()
        self.music_info.setSpacing(0)
        self.title_label = QLabel(self.name)
        self.title_label.setStyleSheet("font-weight: bold")
        self.artist_label = QLabel(self.artist)

        self.music_info.addWidget(self.title_label)
        self.music_info.addWidget(self.artist_label)

        self.view.addLayout(self.music_info)
        self.view.addStretch()

        self.setLayout(self.view)

    def set_highlight(self):
        self.setStyleSheet("background-color: lightblue")

    def clear_highlight(self):
        self.setStyleSheet("")

    def mousePressEvent(self, ev, QMouseEvent=None):
        self.signal.clicked.emit(self.id) # Unnecessary wrapper for testing, real data won't need this
        
class MusicEntryGroup(QWidget):
    def __init__(self):
        super().__init__()

        self.collection = {}
        self.prev = None
        self.current = None

    def add(self, id, obj):
        logger.debug(id)
        self.collection[id] = obj
        obj.signal.clicked.connect(self.on_entry_click)

    def on_entry_click(self, id):
        self.prev = self.current
        self.current = self.collection[id]

        self.current.set_highlight()
        if self.prev is not None and self.prev != self.current:
            self.prev.clear_highlight()


