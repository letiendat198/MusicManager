from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.presenters.MusicListViewPresenter import MusicListViewPresenter
from src.views.components.MusicEntry import *
from src.utils.Signals import EventSignal


class MusicListView(QScrollArea):
    # Init self components first, then initiate other modules
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_signal = EventSignal()

        self.presenter = MusicListViewPresenter(self)
        self.presenter.control_signal.update.connect(self.on_update)

        self.initUI()

    # UI declaration
    def initUI(self):
        self.setWidgetResizable(True)
        # self.setFixedWidth(200)

        self.view = QVBoxLayout(self)
        self.view.setAlignment(Qt.AlignTop)
        self.view.setSpacing(0)

        self.default_label = QLabel("Nothing yet!", parent=self)
        self.view.addWidget(self.default_label)

        self.music_entry_group = MusicEntryGroup(self)
        self.view.addWidget(self.music_entry_group)

        self.widget = QWidget(self)
        self.widget.setLayout(self.view)
        self.setWidget(self.widget)

        self.event_signal.ready.emit()

    def on_update(self, data):
        self.default_label.hide()
        id = data["id"]
        name = data["name"]
        artist = data["artist"]
        mode = data["mode"]
        img = data["img"]

        if id in self.music_entry_group:
            music_entry = self.music_entry_group.get(id)
            music_entry.update_all(name, artist, mode, img)
        else:
            music_entry = MusicEntry(id, name, artist, mode, img=img, parent=self)
            self.music_entry_group.add(id, music_entry)
            music_entry.event_signal.clicked.connect(self.on_music_entry_clicked)

        self.view.addWidget(music_entry)

    def on_music_entry_clicked(self, id):
        self.event_signal.clicked.emit(id)
