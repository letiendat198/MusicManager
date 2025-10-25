from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.utils.DatabaseHelper import TrackObj
from src.utils.Signals import EventSignal
from src.presenters.InfoViewPresenter import InfoViewPresenter
from src.views.components.Separators import HLine
from src.views.components.SpecialLabels import ClickableImageLabel, ScrollableLabel


class InfoView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.event_signal = EventSignal()

        self.presenter = InfoViewPresenter(self)
        self.presenter.control_signal.update.connect(self.populate)

        self.initUI()

    def initUI(self):

        self.setWidgetResizable(True)

        self.view = QFormLayout()

        # self.path_chooser = GenericPathChooser("Choose a folder to save", "Save path")
        # self.search_popup = GetYtUrlPopup()

        self.image_row = QHBoxLayout()
        self.image = ClickableImageLabel()
        self.image.set_image_from_file("resources/placeholder.jpg")
        # self.image.event_signal.clicked.connect(self.on_image_click)

        self.info_side = QFormLayout()
        self.name_edit = QLineEdit()
        self.info_side.addRow("Track name", self.name_edit)
        self.artist_edit = QLineEdit()
        self.info_side.addRow("Artist", self.artist_edit)
        self.album_edit = QLineEdit()
        self.info_side.addRow("Album", self.album_edit)
        self.image_row.addWidget(self.image)
        self.image_row.addLayout(self.info_side)

        self.view.addRow(self.image_row)

        self.view.addRow(HLine())

        self.yt_link_row = QHBoxLayout()
        self.yt_link_edit = QLineEdit()
        self.yt_search_but = QPushButton("Search")
        self.yt_link_row.addWidget(self.yt_link_edit)
        self.yt_link_row.addWidget(self.yt_search_but)
        self.view.addRow("Youtube Link", self.yt_link_row)

        self.title_row = QHBoxLayout()
        self.yt_title = ScrollableLabel()
        self.yt_title_refresh = QPushButton("Refresh")
        self.title_row.addWidget(self.yt_title)
        # self.title_row.addStretch()
        self.title_row.addWidget(self.yt_title_refresh)
        self.view.addRow("Youtube Video Title:", self.title_row)

        self.path_row = QHBoxLayout()
        self.path_label = ScrollableLabel()
        self.path_row.addWidget(self.path_label)
        # self.path_row.addStretch()
        self.path_add_but = QPushButton("Choose")
        self.path_row.addWidget(self.path_add_but)
        self.view.addRow("File path:", self.path_row)


        self.button_row = QHBoxLayout()
        self.save_but = QPushButton("Save")
        self.button_row.addWidget(self.save_but)
        self.download_but = QPushButton("Download")
        self.button_row.addWidget(self.download_but)
        self.delete_but = QPushButton("Delete")
        self.button_row.addWidget(self.delete_but)

        # self.save_but.clicked.connect(self.on_save_click)

        self.view.addRow(self.button_row)

        self.widget = QWidget()
        self.widget.setLayout(self.view)
        self.setWidget(self.widget)

        # self.delete_but.clicked.connect(lambda: self.on_delete_click(self.callback))
        # self.download_but.clicked.connect(lambda: self.on_download_click(self.callback, self.populate, self.threadpool))
        # self.yt_search_but.clicked.connect(lambda: self.on_search_click(self.populate, self.threadpool))
        # self.yt_title_refresh.clicked.connect(lambda: self.on_refresh_click(self.populate, self.threadpool))
        # self.path_add_but.clicked.connect(lambda: self.on_add_path_click(self.populate, self.id))


    def populate(self, track_obj: TrackObj):
        self.name_edit.setText(track_obj.song_name)
        self.artist_edit.setText(track_obj.song_artists)
        self.album_edit.setText(track_obj.album_name)
        self.image.set_image_from_file(track_obj.album_img_path)


    # def on_image_click(self):
    #     self.image_chooser = ImageChooserPopup(self.populate, self.id)
    #
    # def on_save_click(self):
    #     f = FileHelper("data.json")
    #     tracks = json.loads(f.read())
    #     tracks[self.id]["name"] = self.name_edit.text()
    #     tracks[self.id]["artist"] = self.artist_edit.text()
    #     tracks[self.id]["album"] = self.album_edit.text()
    #     tracks[self.id]["yt-url"] = self.yt_link_edit.text()
    #     tracks[self.id]["yt-title"] = self.yt_title.text()
    #     js = json.dumps(tracks)
    #     f.overwrite(js)
    #
    #     if "download-path" in tracks[self.id]:
    #         path = tracks[self.id]["download-path"]
    #         metadata = MetadataHelper(path)
    #         metadata.write(tracks[self.id])
    #         # if "album-image-url" in tracks[self.id]:
    #         #     if tracks[self.id]["album-image-url"] != "":
    #         #         metadata.add_image_from_url(tracks[self.id]["album-image-url"])
    #
    # def on_delete_click(self, update_callback):
    #     f = FileHelper("data.json")
    #     tracks = json.loads(f.read())
    #     if "download-path" in tracks[self.id]:
    #         path = tracks[self.id]["download-path"]
    #         tf = FileHelper(path)
    #         if tf.exists():
    #             print("Downloaded file found, removing", path)
    #             tf.delete()
    #     print("Deleting", tracks[self.id]["name"])
    #     DataManager().delete_entry(self.id)
    #     update_callback()
    #
    # def on_download_click(self, refresh_list, refresh_view, threadpool):
    #     if self.yt_link_edit.text() != "":
    #         self.path_chooser.update_params(DownloadYtPopup,self.yt_link_edit.text(), self.name_edit.text(), self.id,
    #                                         callback1=refresh_list, callback2=refresh_view, threadpool=threadpool)
    #         self.path_chooser.show()
    #     else:
    #         self.error_popup = GenericConfirmPopup("Error", "No Youtube URL", print)
    #         self.error_popup.show()
    #
    # def on_search_click(self, fn, threadpool):
    #     self.search_popup.update_params(self.id, self.name_edit.text(), fn, threadpool)
    #     self.search_popup.show()
    #
    # def on_refresh_click(self, callback, threadpool):
    #     self.yt_title.setText("")
    #     if self.yt_link_edit.text() != "":
    #         self.refresh_popup = YtTitleRefreshPopup(self.id, self.yt_link_edit.text(), callback, threadpool)
    #     else:
    #         self.error_popup = GenericConfirmPopup("Error", "No Youtube URL", print)
    #         self.error_popup.show()
    #
    # def on_add_path_click(self, callback, id):
    #     self.mp3_choose = Mp3ChooserPopup(callback, id)