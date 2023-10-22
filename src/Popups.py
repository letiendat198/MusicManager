import sys
import json
import YoutubeHandler

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SpotifyHandler import *

from FileHelper import *
from ThreadWorker import Worker


class ImportSpotifyPopup(QWidget):
    def __init__(self, callback_fn, threadpool):
        super(ImportSpotifyPopup, self).__init__()

        self.threadpool = threadpool

        self.setWindowTitle("Import from Spotify")
        self.setFixedWidth(350)

        self.view = QFormLayout()

        self.id_input = QLineEdit()
        self.secret_input = QLineEdit()
        self.view.addRow("Client ID", self.id_input)
        self.view.addRow("Client Secret", self.secret_input)

        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.on_click)
        self.view.addRow(self.submit)

        self.f = FileHelper("secrets.json")
        if self.f.exists():
            self.cache = json.loads(self.f.read())
            self.id_input.setText(self.cache["client_id"])
            self.secret_input.setText(self.cache["client_secret"])

        self.setLayout(self.view)

        self.callback_fn = callback_fn

    def on_click(self):
        self.loading_popup = GenericTextPopup("Working", "Working on it")
        self.loading_popup.show()
        if not self.f.exists():
            js = {
                "client_id": self.id_input.text(),
                "client_secret": self.secret_input.text()
            }
            self.f.write(json.dumps(js))
        elif self.id_input.text() != self.cache["client_id"] or self.secret_input.text() != self.cache["client_secret"]:
            js = {
                "client_id": self.id_input.text(),
                "client_secret": self.secret_input.text()
            }
            self.f.overwrite(json.dumps(js))

        self.spotify_handler = SpotifyHandler(self.id_input.text(), self.secret_input.text())

        self.worker = Worker(self.spotify_handler.get_liked_track)
        self.worker.signal.finished.connect(self.on_finish)
        self.worker.signal.progress.connect(self.on_progress)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)
        self.close()

    def on_progress(self, progress):
        self.loading_popup.set_text("Found " + str(progress) + " songs")

    def on_finish(self):
        self.success_popup = GenericConfirmPopup("Success", "Successfully get liked tracks from Spotify",
                                                 self.callback_fn)
        self.success_popup.show()
        self.loading_popup.close()

    def on_error(self, trace):
        self.success_popup = GenericConfirmPopup("Error", str(trace), self.callback_fn)
        self.success_popup.show()
        self.loading_popup.close()


class BatchGetYtUrlPopup(QWidget):
    def __init__(self, threadpool):
        super(BatchGetYtUrlPopup, self).__init__()

        self.setFixedWidth(500)

        self.threadpool = threadpool
        self.success_count = 0
        self.error_count = 0

        self.setWindowTitle("Getting Youtube URLs")

        self.view = QVBoxLayout()

        self.label = QLabel("Got {success} urls\nFailed: {fail}".format(success=self.success_count, fail=self.error_count))
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        self.process_entries()

    def process_entries(self):
        self.f = FileHelper("liked.json")
        tracks = json.loads(self.f.read())
        for track in tracks:
            self.get_url_for_entry(track, tracks[track]["artist"])

    def get_url_for_entry(self, name, artist):
        self.worker = Worker(YoutubeHandler.get_url, name, name + " " + artist + " lyrics")
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)

    def on_update(self):
        self.label.setText("Got {success} urls\nFailed: {fail}".format(success=self.success_count, fail=self.error_count))

    def on_result(self, res):
        self.success_count += 1
        name = res[0]
        link = res[1]
        title = res[2]
        tracks = json.loads(self.f.read())
        obj = {
            name: {
                "artist": tracks[name]["artist"],
                "id": tracks[name]["id"],
                "yt-url": link,
                "yt-title": title
            }
        }
        tracks.update(obj)
        js = json.dumps(tracks)
        self.f.overwrite(js)
        self.on_update()

    def on_error(self):
        self.error_count += 1
        self.on_update()


class GetYtUrlPopup(QWidget):
    def __init__(self, name, fn, threadpool):
        super(GetYtUrlPopup, self).__init__()

        self.fn = fn
        self.threadpool = threadpool
        self.name = name

        self.setWindowTitle("Search for Youtube URL")

        self.view = QFormLayout()

        self.keyword = QLineEdit(name)
        self.view.addRow("Search Keywords", self.keyword)

        self.conf_but = QPushButton("Confirm")
        self.conf_but.clicked.connect(self.on_click)
        self.view.addWidget(self.conf_but)

        self.setLayout(self.view)

        self.loading_popup = GenericTextPopup("Searching for URL", "Searching")

    def on_click(self):
        self.loading_popup.show()
        self.worker = Worker(YoutubeHandler.get_url, self.name, self.keyword.text())
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)
        self.close()

    def on_result(self, res):
        f = FileHelper("liked.json")
        name = res[0]
        link = res[1]
        title = res[2]
        tracks = json.loads(f.read())
        obj = {
            name: {
                "artist": tracks[name]["artist"],
                "id": tracks[name]["id"],
                "yt-url": link,
                "yt-title": title
            }
        }
        tracks.update(obj)
        js = json.dumps(tracks)
        f.overwrite(js)
        self.loading_popup.close()
        self.success_popup = GenericConfirmPopup("Success", "URL found", self.fn, self.name)
        self.success_popup.show()

    def on_error(self, trace):
        self.error_popup = GenericConfirmPopup("Error", str(trace), print)
        self.error_popup.show()
        self.close()


class DownloadYtPopup(QWidget):
    def __init__(self, url, name, threadpool):
        super(DownloadYtPopup, self).__init__()

        self.setFixedWidth(500)

        self.threadpool = threadpool
        self.url = url
        self.name = name

        self.setWindowTitle("Downloading music")

        self.view = QVBoxLayout()

        self.label = QLabel("Downloading")
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        self.fail_popup = GenericConfirmPopup("Error", "No Youtube URL", print)
        self.success_popup = GenericConfirmPopup("Success", "Download completed", print)
        self.start_task()

    def start_task(self):
        if self.url != "":
            self.worker = Worker(YoutubeHandler.download, self.url, self.name)
            self.worker.signal.finished.connect(self.on_finish)
            self.worker.signal.error.connect(self.on_error)
            self.threadpool.start(self.worker)
        else:
            self.fail_popup.show()
            self.close()

    def on_finish(self):
        self.success_popup.show()
        self.close()

    def on_error(self, trace):
        self.error_popup = GenericConfirmPopup("Error", str(trace), print)
        self.error_popup.show()
        self.close()


class GenericConfirmPopup(QWidget):
    def __init__(self, title, label, fn, *args, **kwargs):
        super(GenericConfirmPopup, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.setWindowTitle(title)

        self.view = QVBoxLayout()

        self.label = QLabel(label)
        self.view.addWidget(self.label)

        self.confirm = QPushButton("OK")
        self.confirm.clicked.connect(self.on_click)
        self.view.addWidget(self.confirm)

        self.setLayout(self.view)

    def on_click(self):
        self.fn(*self.args, **self.kwargs)
        self.close()


class GenericTextPopup(QWidget):
    def __init__(self, title, label):
        super(GenericTextPopup, self).__init__()

        self.setWindowTitle(title)

        self.view = QVBoxLayout()

        self.label = QLabel(label)
        self.view.addWidget(self.label)

        self.setLayout(self.view)

    def set_text(self, progress):
        self.label.setText(progress)
