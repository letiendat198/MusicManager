from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class InfoEditingPanel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.view = QFormLayout()

        self.default_off = False
        self.default_label = QLabel("No info to show")
        self.view.addWidget(self.default_label)

        self.widget = QWidget()
        self.widget.setLayout(self.view)
        self.setWidget(self.widget)

        # self.path_chooser = GenericPathChooser("Choose a folder to save", "Save path")
        # self.search_popup = GetYtUrlPopup()

    # def switch_off_default(self):
    #     self.default_off = True
    #
    #     self.default_label.hide()
    #
    #     self.image_row = QHBoxLayout()
    #     self.image = ImageLabel()
    #     self.image.set_image_from_file("resources/placeholder.jpg")
    #     self.image.signal.clicked.connect(self.on_image_click)
    #
    #     self.info_side = QFormLayout()
    #     self.name_edit = QLineEdit()
    #     self.info_side.addRow("Track name", self.name_edit)
    #     self.artist_edit = QLineEdit()
    #     self.info_side.addRow("Artist", self.artist_edit)
    #     self.album_edit = QLineEdit()
    #     self.info_side.addRow("Album", self.album_edit)
    #     self.image_row.addWidget(self.image)
    #     self.image_row.addLayout(self.info_side)
    #
    #     self.view.addRow(self.image_row)
    #
    #     self.view.addRow(HLine())
    #
    #     self.yt_link_row = QHBoxLayout()
    #     self.yt_link_edit = QLineEdit()
    #     self.yt_search_but = QPushButton("Search")
    #     self.yt_link_row.addWidget(self.yt_link_edit)
    #     self.yt_link_row.addWidget(self.yt_search_but)
    #     self.view.addRow("Youtube Link", self.yt_link_row)
    #
    #     self.title_row = QHBoxLayout()
    #     self.yt_title = ScrollableLabel()
    #     self.yt_title_refresh = QPushButton("Refresh")
    #     self.title_row.addWidget(self.yt_title)
    #     # self.title_row.addStretch()
    #     self.title_row.addWidget(self.yt_title_refresh)
    #     self.view.addRow("Youtube Video Title:", self.title_row)
    #
    #     self.path_row = QHBoxLayout()
    #     self.path_label = ScrollableLabel()
    #     self.path_row.addWidget(self.path_label)
    #     # self.path_row.addStretch()
    #     self.path_add_but = QPushButton("Choose")
    #     self.path_row.addWidget(self.path_add_but)
    #     self.view.addRow("File path:", self.path_row)
    #
    #
    #     self.button_row = QHBoxLayout()
    #     self.save_but = QPushButton("Save")
    #     self.button_row.addWidget(self.save_but)
    #     self.download_but = QPushButton("Download")
    #     self.button_row.addWidget(self.download_but)
    #     self.delete_but = QPushButton("Delete")
    #     self.button_row.addWidget(self.delete_but)
    #
    #     self.save_but.clicked.connect(self.on_save_click)
    #
    #     self.view.addRow(self.button_row)
    #
    #     self.delete_but.clicked.connect(lambda: self.on_delete_click(self.callback))
    #     self.download_but.clicked.connect(lambda: self.on_download_click(self.callback, self.populate, self.threadpool))
    #     self.yt_search_but.clicked.connect(lambda: self.on_search_click(self.populate, self.threadpool))
    #     self.yt_title_refresh.clicked.connect(lambda: self.on_refresh_click(self.populate, self.threadpool))
    #     self.path_add_but.clicked.connect(lambda: self.on_add_path_click(self.populate, self.id))
    #
    # def save_for_later(self, callback, threadpool):
    #     self.callback = callback
    #     self.threadpool = threadpool
    #
    # def populate(self, id):
    #     print(id)
    #     self.id = id
    #     if not self.default_off:
    #         self.switch_off_default()
    #
    #     f = FileHelper("data.json")
    #     tracks = json.loads(f.read())
    #     self.name_edit.setText(tracks[id]["name"])
    #     self.artist_edit.setText(tracks[id]["artist"])
    #     self.album_edit.setText(tracks[id]["album"])
    #     self.image.set_image_from_file("resources/placeholder.jpg")
    #     self.path_label.setText("")
    #     if "yt-url" in tracks[id]:
    #         self.yt_link_edit.setText(tracks[id]["yt-url"])
    #         self.yt_link_edit.setCursorPosition(0)
    #         self.yt_title.setText(tracks[id]["yt-title"])
    #         self.yt_title.setCursorPosition(0)
    #     else:
    #         self.yt_link_edit.setText("")
    #         self.yt_title.setText("")
    #     if "download-path" in tracks[id]:
    #         self.path_label.setText(tracks[id]["download-path"])
    #         self.path_label.setCursorPosition(0)
    #         img_data = MetadataHelper(tracks[id]["download-path"]).get_album_image()
    #         if img_data is not None:
    #             print("Loading image from local file")
    #             self.image.set_image_from_data(img_data)
    #     elif "album-image-url" in tracks[id] and tracks[id]["album-image-url"] != "":
    #         url = tracks[id]["album-image-url"]
    #         print("Fetching image via url", url)
    #         try:
    #             http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=2.0, read=2.0))
    #             resp = http.request("GET", url)
    #             self.image.set_image_from_data(resp.data)
    #         except Exception as e:
    #             print(e)
    #
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