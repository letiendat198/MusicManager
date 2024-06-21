import sys
import logging

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication

from src.views.InfoView import InfoEditingPanel
from src.views.MusicListView import MusicListView
from src.views.components.MenuBar import MenuBar
# from src.views.popups.Popups import *

from src.utils.DataManager import *
from src.utils.SettingsManager import *

logging.basicConfig(level=logging.NOTSET)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.MenuBar = MenuBar()
        self.setMenuBar(self.MenuBar)

        self.setWindowTitle("Music Manager")
        self.resize(1300, 800)

        main_layout = QHBoxLayout()

        self.side_media_list = MusicListView()
        self.info_editing_panel = InfoEditingPanel()

        main_layout.addWidget(self.side_media_list, 45)
        main_layout.addWidget(self.info_editing_panel, 65)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # self.info_editing_panel.save_for_later(self.update_tracks, self.threadpool)

    #     self.update_tracks()
    #
    # def update_tracks(self):
    #     self.side_media_list.populate()
    #     for button in self.side_media_list.media_button_list:
    #         button.connect(self.info_editing_panel.populate)

# class MediaTitleButton(QPushButton):
#     def __init__(self, label, id):
#         super(MediaTitleButton, self).__init__()
#
#         self.id = id
#         self.setText(label)
#         self.setStyleSheet("QPushButton { text-align: left; border: 0px; font-size: 15px; padding: 5px} "
#                            "QPushButton:checked { text-align: left; border: 0px; font-size: 15px; padding: 5px; "
#                            "background-color:lightblue}")
#         self.setCheckable(True)
#
#     def set_downloaded(self):
#         self.setStyleSheet(
#             "QPushButton { text-align: left; border: 0px; font-size: 15px; padding: 5px; background-color:lightgreen} "
#             "QPushButton:checked { text-align: left; border: 0px; font-size: 15px; padding: 5px; "
#             "background-color:limegreen}")
#
#     def set_normal(self):
#         self.setStyleSheet("QPushButton { text-align: left; border: 0px; font-size: 15px; padding: 5px} "
#                            "QPushButton:checked { text-align: left; border: 0px; font-size: 15px; padding: 5px; "
#                            "background-color:lightblue}")
#
#     def connect(self, fn):
#         self.clicked.connect(lambda: fn(self.id))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
