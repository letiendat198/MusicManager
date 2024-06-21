from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.presenters.MusicListViewPresenter import MusicListViewPresenter
from src.views.components.MusicEntry import *
from src.utils.Signals import EventSignal


class MusicListView(QScrollArea):
    # Init self components first, then initiate other modules
    def __init__(self):
        super().__init__()
        self.event_signal = EventSignal()

        self.presenter = MusicListViewPresenter(self)

        self.presenter.control_signal.update.connect(self.on_update)

        self.initUI()

    # UI declaration
    def initUI(self):
        self.setWidgetResizable(True)
        # self.setFixedWidth(200)

        self.view = QVBoxLayout()
        self.view.setAlignment(Qt.AlignTop)

        self.default_label = QLabel("Nothing yet!")
        self.view.addWidget(self.default_label)

        self.music_entry_group = MusicEntryGroup()
        self.view.addWidget(self.music_entry_group)

        self.widget = QWidget()
        self.widget.setLayout(self.view)
        self.setWidget(self.widget)

        self.event_signal.ready.emit()

    def on_update(self, data):
        self.default_label.hide()

        for entries in data:
            self.music_entry = MusicEntry(entries, data[entries]["name"], data[entries]["img_data"], data[entries]["artist"])
            self.music_entry_group.add(entries, self.music_entry)

            self.view.addWidget(self.music_entry)
