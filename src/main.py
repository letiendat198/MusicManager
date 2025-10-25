import sys
import logging

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication

from src.mediators.InfoViewMediator import InfoViewMediator
from src.views.InfoView import InfoView
from src.views.MusicListView import MusicListView
from src.views.components.MenuBar import MenuBar
import src.thread_manager.ThreadManager as ThreadManager
import src.cache_manager.CacheManager

logging.basicConfig(level=logging.INFO)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.MenuBar = MenuBar(self)
        self.setMenuBar(self.MenuBar)

        self.setWindowTitle("Music Manager")
        self.resize(1300, 800)

        main_layout = QHBoxLayout()

        self.music_list_view = MusicListView(self)
        self.info_view = InfoView(self)

        self.mediator = InfoViewMediator(self.music_list_view.presenter, self.info_view.presenter)

        main_layout.addWidget(self.music_list_view, 45)
        main_layout.addWidget(self.info_view, 65)

        main_widget = QWidget(self)
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
