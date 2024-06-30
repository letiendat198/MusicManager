from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.views.popups.ImportSpotifyPopup import ImportSpotifyPopup


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        fileMenu = QMenu("File", self)
        importMenu = fileMenu.addMenu("Import")
        self.action_import_json = QAction("Import from JSON...", importMenu)
        importMenu.addAction(self.action_import_json)
        self.action_import_spotify = QAction("Import from Spotify...", importMenu)
        importMenu.addAction(self.action_import_spotify)

        addMenu = fileMenu.addMenu("Add")
        self.action_add_sp_playlist = QAction("Add a Spotify playlist...", addMenu)
        addMenu.addAction(self.action_add_sp_playlist)
        self.action_add_yt = QAction("Add a Youtube video...", addMenu)
        addMenu.addAction(self.action_add_yt)
        self.action_add_yt_playlist = QAction("Add a Youtube playlist...", addMenu)
        addMenu.addAction(self.action_add_yt_playlist)
        self.addMenu(fileMenu)

        self.action_set_download_path = QAction("Match existing files...", fileMenu)
        fileMenu.addAction(self.action_set_download_path)

        self.action_open_settings = QAction("Settings...", fileMenu)
        fileMenu.addAction(self.action_open_settings)

        editMenu = QMenu("Action", self)
        self.action_refresh = QAction("Refresh", editMenu)
        editMenu.addAction(self.action_refresh)
        self.action_batch_get_yt_link = QAction("Batch: Get Youtube Urls", editMenu)
        editMenu.addAction(self.action_batch_get_yt_link)
        self.action_batch_download_yt = QAction("Batch: Download from Youtube", editMenu)
        editMenu.addAction(self.action_batch_download_yt)
        self.action_batch_write_metadata = QAction("Batch: Write metadata to downloaded files", editMenu)
        editMenu.addAction(self.action_batch_write_metadata)
        self.addMenu(editMenu)

        self.connect_actions()

    def connect_actions(self):
        # self.action_import_json.triggered.connect()
        self.action_import_spotify.triggered.connect(self.open_import_spotify_popup)
        # self.action_add_sp_playlist.triggered.connect(lambda: self.open_add_sp_playlist(fn, threadpool))
        # self.action_add_yt.triggered.connect(lambda: self.open_add_yt(fn, threadpool))
        # self.action_add_yt_playlist.triggered.connect(lambda: self.open_add_yt_playlist(fn, threadpool))
        # self.action_batch_get_yt_link.triggered.connect(lambda: self.open_batch_get_yt_url_popup(threadpool))
        # self.action_batch_download_yt.triggered.connect(lambda: self.open_batch_download_yt_popup(fn, threadpool))
        # self.action_batch_write_metadata.triggered.connect(lambda: self.open_batch_write_metadata_popup(threadpool))
        # self.action_refresh.triggered.connect(lambda: self.on_refresh(fn))
        # self.action_set_download_path.triggered.connect(lambda: self.open_set_dl_path(fn, threadpool))
        # self.action_open_settings.triggered.connect(self.open_settings)

    # def on_refresh(self, fn):
    #     DataManager().update().validate_download()
    #     fn()

    def open_import_spotify_popup(self):
        self.import_spotify_popup = ImportSpotifyPopup()

    # def open_add_sp_playlist(self, fn, threadpool):
    #     self.add_sp_playlist_popup = AddSpotifyPlaylistPopup(fn, threadpool)
    #     self.add_sp_playlist_popup.show()
    #
    # def open_add_yt(self, fn, threadpool):
    #     self.add_yt_popup = AddYtVideoPopup(fn, threadpool)
    #     self.add_yt_popup.show()
    #
    # def open_add_yt_playlist(self, fn, threadpool):
    #     self.add_yt_playlist_popup = AddYtPlaylistPopup(fn, threadpool)
    #     self.add_yt_playlist_popup.show()
    # def open_set_dl_path(self, fn, threadpool):
    #     self.choose_path_popup = GenericPathChooser("Choose a folder contains existing files", "Choose path")
    #     self.choose_path_popup.update_params(SetExistingPath, callback=fn, threadpool=threadpool)
    #     self.choose_path_popup.show()
    #
    # def open_settings(self):
    #     self.settings_menu = SettingsMenu()
    #     self.settings_menu.show()
    # def open_batch_get_yt_url_popup(self, threadpool):
    #     self.batch_get_yt_url_popup = BatchGetYtUrlPopup(threadpool)
    #     self.batch_get_yt_url_popup.show()
    #
    # def open_batch_download_yt_popup(self, callback, threadpool):
    #     self.batch_download_yt = GenericPathChooser("Choose a folder to save", "Save path")
    #     self.batch_download_yt.update_params(BatchDownloadYtPopup, callback=callback, threadpool=threadpool)
    #     self.batch_download_yt.show()
    #
    # def open_batch_write_metadata_popup(self, threadpool):
    #     self.batch_write_metadata = BatchWriteMetadataPopup(threadpool)
    #     self.batch_write_metadata.show()