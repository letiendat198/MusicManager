from src.services import YoutubeHandler

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from src.services.SpotifyHandler import *

from src.thread_manager.ThreadWorker import Worker
from src.utils.DataManager import *
from src.utils.MetadataHelper import *
from src.utils.SettingsManager import *
from src.utils.LanguageHelper import *

language_helper = LanguageHelper("en_us")
_ = language_helper.get
settings = SettingsManager()



class AddSpotifyPlaylistPopup(QWidget):
    def __init__(self, callback_fn, threadpool):
        super(AddSpotifyPlaylistPopup, self).__init__()

        self.threadpool = threadpool

        self.setWindowTitle("Add a playlist from Spotify")
        self.setFixedWidth(350)
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QFormLayout()

        self.id_input = QLineEdit()
        self.secret_input = QLineEdit()
        self.playlist_id = QLineEdit()
        self.view.addRow("Client ID", self.id_input)
        self.view.addRow("Client Secret", self.secret_input)
        self.view.addRow("Playlist ID", self.playlist_id)

        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.on_click)
        self.view.addRow(self.submit)

        self.f = FileHelper("../../secrets.json")
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

        self.worker = Worker(self.spotify_handler.get_playlist_track, self.playlist_id.text())
        self.worker.signal.finished.connect(self.on_finish)
        self.worker.signal.progress.connect(self.on_progress)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)
        self.close()

    def on_progress(self, progress):
        self.loading_popup.set_text("Found " + str(progress) + " songs")

    def on_finish(self):
        self.success_popup = GenericConfirmPopup("Success", "Successfully get playlist from Spotify",
                                                 self.callback_fn)
        self.success_popup.show()
        self.loading_popup.close()

    def on_error(self, trace):
        self.success_popup = GenericConfirmPopup("Error", str(trace), self.callback_fn)
        self.success_popup.show()
        self.loading_popup.close()


class AddYtVideoPopup(QWidget):
    def __init__(self, callback, threadpool):
        super(AddYtVideoPopup, self).__init__()

        self.fn = callback
        self.threadpool = threadpool

        self.setWindowTitle("Add a Youtube video")
        self.setFixedWidth(350)
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QFormLayout()

        self.video_url = QLineEdit()
        self.view.addRow("Video URL", self.video_url)

        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.on_click)
        self.view.addWidget(self.submit)

        self.setLayout(self.view)

    def on_click(self):
        self.loading_popup = GenericTextPopup("Working", "Working on it")
        self.loading_popup.show()

        self.worker = Worker(YoutubeHandler.get_info, "placeholder_id", self.video_url.text())
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)
        self.close()

    def on_result(self, res):
        id = res[1]
        title = res[2]
        url = res[3]

        f = FileHelper("../../Youtube.json")
        if not f.exists():
            f.write("{}")
        tracks = json.loads(f.read())

        tracks[id] = {
            "name": title,
            "artist": "",
            "album": "",
            "album-image-url": "",
            "source": "Youtube",
            "yt-url": url,
            "yt-title": title
        }
        js = json.dumps(tracks)
        f.overwrite(js)
        DataManager().add_source("Youtube.json").update()

        self.success_popup = GenericConfirmPopup("Youtube video added", "Added " + title + " to library",
                                                 self.fn)
        self.success_popup.show()
        self.loading_popup.close()

    def on_error(self, trace):
        self.success_popup = GenericConfirmPopup("Error", str(trace), self.callback_fn)
        self.success_popup.show()
        self.loading_popup.close()


class AddYtPlaylistPopup(QWidget):
    def __init__(self, callback, threadpool):
        super(AddYtPlaylistPopup, self).__init__()

        self.fn = callback
        self.threadpool = threadpool

        self.setWindowTitle("Add a Youtube playlist")
        self.setFixedWidth(400)
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QFormLayout()

        self.video_url = QLineEdit()
        self.view.addRow("Playlist URL", self.video_url)

        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.on_click)
        self.view.addWidget(self.submit)

        self.setLayout(self.view)

    def on_click(self):
        self.loading_popup = GenericTextPopup("Working", "Working on it")
        self.loading_popup.show()

        self.worker = Worker(YoutubeHandler.get_playlist_info, self.video_url.text())
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)
        self.close()

    def on_result(self, res):
        title = res[0]
        data = res[1]

        f = FileHelper(title + ".json")
        js = json.dumps(data)
        f.overwrite(js)
        DataManager().add_source(title + ".json").update()

        self.success_popup = GenericConfirmPopup("Youtube playlist added", "Added " + title + " to library",
                                                 self.fn)
        self.success_popup.show()
        self.loading_popup.close()

    def on_error(self, trace):
        self.success_popup = GenericConfirmPopup("Error", str(trace), self.callback_fn)
        self.success_popup.show()
        self.loading_popup.close()


class SetExistingPath(QWidget):
    def __init__(self, path, callback, threadpool):
        super(SetExistingPath, self).__init__()
        self.path = path
        self.threadpool = threadpool
        self.callback = callback

        self.success_count = 0
        self.error_count = 0
        self.total = 0

        self.setWindowTitle("Matching files...")

        self.view = QVBoxLayout()

        self.label = QLabel(
            "Matched {success}/{total} files\nFailed to match: {fail} files".format(success=self.success_count,
                                                                                    fail=self.error_count,
                                                                                    total=self.total))
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        self.queue = []

        f = FileHelper("../../data.json")
        self.entries = json.loads(f.read())
        self.process_entries()

    def process_entries(self):
        for file in os.listdir(self.path):
            if file.endswith(".mp3"):
                self.total += 1
                self.on_update()
        for file in os.listdir(self.path):
            if file.endswith(".mp3"):
                self.start_search_task(file)

    def start_search_task(self, file):
        self.worker = Worker(self.search_in_entries, self.entries, file)
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)

    def search_in_entries(self, entries, filename, progress_callback):
        for id in entries:
            save_name = entries[id]["name"] + "-" + entries[id]["artist"] + ".mp3"
            save_name = re.sub('[\\/?:*"<>|]', '', save_name)
            if filename == save_name:
                return id, filename
            print(save_name)
        print("Failed:", filename)
        raise Exception("No matching entry")

    def on_result(self, res):
        id = res[0]
        name = res[1]
        self.queue.append((id, name))
        self.success_count += 1
        self.on_update()

    def on_error(self):
        self.error_count += 1
        self.on_update()

    def on_update(self):
        self.label.setText(
            "Matched {success}/{total} files\nFailed to match: {fail} files".format(success=self.success_count,
                                                                                    fail=self.error_count,
                                                                                    total=self.total))
        if self.success_count + self.error_count == self.total:
            # self.label.setText("Writing changes...")
            f = FileHelper("../../data.json")
            entries = json.loads(f.read())
            for entry in self.queue:
                entries[entry[0]]["download-path"] = os.path.join(self.path, entry[1])
            js = json.dumps(entries)
            f.overwrite(js)

            self.callback()
            self.close()


class BatchGetYtUrlPopup(QWidget):
    def __init__(self, threadpool):
        super(BatchGetYtUrlPopup, self).__init__()

        self.setFixedWidth(350)

        self.threadpool = threadpool
        self.success_count = 0
        self.error_count = 0
        self.finished_count = 0
        self.total = 0

        self.setWindowTitle("Getting Youtube URLs")

        self.view = QVBoxLayout()

        self.label = QLabel(
            "Got {success} urls\nFailed: {fail}".format(success=self.success_count, fail=self.error_count))
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        self.process_entries()

    def process_entries(self):
        # FIXME: BLOCKING
        self.f = FileHelper("../../data.json")
        tracks = json.loads(self.f.read())
        for track in tracks:
            if settings.reload()["skip_have_url"] and "yt-url" in tracks[track] and tracks[track]["yt-url"] != "":
                continue
            self.total += 1
            self.get_url_for_entry(track, tracks[track]["name"], tracks[track]["artist"])

        if self.total == 0:
            self.total += 1
            self.on_finish()

    def get_url_for_entry(self, id, name, artist):
        self.worker = Worker(YoutubeHandler.get_url, id, name + " " + artist + " lyrics")
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.worker.signal.finished.connect(self.on_finish)
        self.threadpool.start(self.worker)

    def on_update(self):
        self.label.setText(
            "Got {success}/{total} urls\nFailed: {fail}".format(success=self.success_count, total=self.total,
                                                                fail=self.error_count))

    def on_result(self, res):
        self.success_count += 1
        id = res[0]
        link = res[1]
        title = res[2]
        tracks = json.loads(self.f.read())
        tracks[id]["yt-url"] = link
        tracks[id]["yt-title"] = title
        js = json.dumps(tracks)
        self.f.overwrite(js)
        self.on_update()

    def on_error(self):
        self.error_count += 1
        self.on_update()

    def on_finish(self):
        self.finished_count += 1
        if self.finished_count == self.total:
            self.finish_popup = GenericConfirmPopup("Get Youtube URLs", "Done", print)
            self.finish_popup.show()
            self.close()


class GetYtUrlPopup(QWidget):
    def __init__(self):
        super(GetYtUrlPopup, self).__init__()

        self.setWindowTitle("Search for Youtube URL")
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QFormLayout()
        self.keyword = QLineEdit()
        self.view.addRow("Search Keywords", self.keyword)

        self.conf_but = QPushButton("Confirm")
        self.conf_but.clicked.connect(self.on_click)
        self.view.addWidget(self.conf_but)

        self.setLayout(self.view)

        self.loading_popup = GenericTextPopup("Searching for URL", "Searching")

    def update_params(self, id, name, fn, threadpool):
        self.fn = fn
        self.threadpool = threadpool
        self.id = id
        self.name = name
        self.keyword.setText(self.name)

    def on_click(self):
        self.loading_popup.show()
        self.worker = Worker(YoutubeHandler.get_url, self.id, self.keyword.text())
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)
        self.close()

    def on_result(self, res):
        f = FileHelper("../../data.json")
        id = res[0]
        link = res[1]
        title = res[2]
        tracks = json.loads(f.read())
        tracks[id]["yt-url"] = link
        tracks[id]["yt-title"] = title
        js = json.dumps(tracks)
        f.overwrite(js)
        self.loading_popup.close()
        self.success_popup = GenericConfirmPopup("Success", "URL found", self.fn, self.id)
        self.success_popup.show()

    def on_error(self, trace):
        self.error_popup = GenericConfirmPopup("Error", str(trace), print)
        self.error_popup.show()
        self.close()


class DownloadYtPopup(QWidget):
    def __init__(self, url, name, id, path, callback1, callback2, threadpool):
        super(DownloadYtPopup, self).__init__()

        self.threadpool = threadpool
        self.url = url
        self.name = name
        self.id = id
        self.path = path
        self.fn = callback1
        self.fn2 = callback2

        self.setWindowTitle("Downloading music")

        self.setWindowModality(Qt.ApplicationModal)

        self.view = QVBoxLayout()

        self.label = QLabel("Downloading")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumWidth(300)
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        self.fail_popup = GenericConfirmPopup("Error", "No Youtube URL", print)
        self.success_popup = GenericConfirmPopup("Success", "Download completed", print)
        self.start_task()

    def start_task(self):
        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        if self.url != "":
            self.worker = Worker(YoutubeHandler.download, self.url, self.name + "-" + tracks[self.id]["artist"],
                                 self.id, self.path)
            self.worker.signal.result.connect(self.on_result)
            self.worker.signal.error.connect(self.on_error)
            self.threadpool.start(self.worker)
        else:
            self.fail_popup.show()
            self.close()

    def on_result(self, res):
        id = res[0]
        path = res[1]
        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        tracks[id]["download-path"] = path
        js = json.dumps(tracks)
        f.overwrite(js)
        metadata = MetadataHelper(path)
        metadata.write(tracks[id])
        if "album-image-url" in tracks[id] and tracks[id]["album-image-url"] != "":
            metadata.add_image_from_url(tracks[self.id]["album-image-url"])
        self.success_popup.show()
        self.fn()
        self.fn2(self.id)
        self.close()

    def on_error(self, trace):
        self.error_popup = GenericConfirmPopup("Error", str(trace), print)
        self.error_popup.show()
        self.close()


class BatchDownloadYtPopup(QWidget):
    def __init__(self, path, callback, threadpool):
        super(BatchDownloadYtPopup, self).__init__()

        self.setFixedWidth(400)
        self.setWindowModality(Qt.ApplicationModal)

        self.threadpool = threadpool
        self.path = path
        self.callback = callback

        self.setWindowTitle("Downloading...")

        self.view = QVBoxLayout()

        self.count = 0
        self.error = 0
        self.total = 0
        self.finished_count = 0

        self.label = QLabel(
            "Successfully downloaded {success}/{total} \nFailed: {error}".format(success=self.count, total=self.total,
                                                                                 error=self.error))
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        self.process_entries()

    def process_entries(self):
        # FIXME: BLOCKING
        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        for track in tracks:
            if settings.reload()["skip_downloaded"] and ("download-path" in tracks[track]) and tracks[track]["download-path"] != "":
                continue
            if "yt-url" in tracks[track]:
                self.total += 1
                self.start_task(tracks[track]["yt-url"], tracks[track]["name"] + "-" + tracks[track]["artist"], track)

    def start_task(self, url, name, id):
        self.worker = Worker(YoutubeHandler.download, url, name, id, self.path)
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.worker.signal.finished.connect(self.on_finish)
        self.threadpool.start(self.worker)

    def on_result(self, res):
        id = res[0]
        path = res[1]
        self.count += 1
        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        tracks[id]["download-path"] = path
        js = json.dumps(tracks)
        f.overwrite(js)
        # metadata = MetadataHelper(path)
        # metadata.write(tracks[id])
        # if "album-image-url" in tracks[id] and tracks[id]["album-image-url"] != "":
        #     metadata.add_image_from_url(tracks[id]["album-image-url"])
        self.on_progress()

    def on_error(self, trace):
        self.error += 1
        self.on_progress()

    def on_progress(self):
        self.label.setText(
            "Successfully downloaded {success}/{total} \nFailed: {error}".format(success=self.count, total=self.total,
                                                                                 error=self.error))

    def on_finish(self):
        self.finished_count += 1
        if self.finished_count == self.total:
            self.finished_popup = GenericConfirmPopup("Download from Youtube", "Done", self.callback)
            self.finished_popup.show()
            self.close()


class YtTitleRefreshPopup:
    def __init__(self, id, url, callback, threadpool):
        self.id = id
        self.url = url
        self.fn = callback
        self.threadpool = threadpool

        self.worker = Worker(YoutubeHandler.get_info, self.id, self.url)
        self.worker.signal.result.connect(self.on_result)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)

    def on_result(self, res):
        id = res[0]
        yt_id = res[1]
        title = res[2]

        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        tracks[id]["yt-title"] = title
        tracks[id]["yt-url"] = self.url
        js = json.dumps(tracks)
        f.overwrite(js)
        self.fn(id)

    def on_error(self, trace):
        self.error_popup = GenericConfirmPopup("Error", str(trace), print)
        self.error_popup.show()


class BatchWriteMetadataPopup(QWidget):
    def __init__(self, threadpool):
        super(BatchWriteMetadataPopup, self).__init__()

        self.setFixedWidth(400)

        self.threadpool = threadpool

        self.setWindowTitle("Writing metadata...")
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QVBoxLayout()

        self.count = 0
        self.error = 0
        self.total = 0

        self.label = QLabel(
            "Successfully written {success}/{total} \nFailed: {error}".format(success=self.count, total=self.total,
                                                                              error=self.error))
        self.view.addWidget(self.label)

        self.setLayout(self.view)

        QCoreApplication.instance().processEvents()
        self.process_entries()

    def process_entries(self):
        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        # FIXME: BLOCKING
        for track in tracks:
            if "download-path" in tracks[track]:
                self.total += 1
                image_url = ""
                if "album-image-url" in tracks[track]:
                    image_url = tracks[track]["album-image-url"]
                self.start_task(tracks[track]["download-path"], tracks[track], image_url)

    def start_task(self, path, obj, url):
        self.worker = Worker(MetadataHelper(path).write, obj)
        if url != "":
            self.worker = Worker(MetadataHelper(path).write_and_add_image, obj, url)
        self.worker.signal.finished.connect(self.on_finish)
        self.worker.signal.error.connect(self.on_error)
        self.threadpool.start(self.worker)

    def on_finish(self):
        self.count += 1
        self.on_progress()

    def on_error(self, trace):
        self.error += 1
        self.on_progress()

    def on_progress(self):
        self.label.setText(
            "Successfully written {success}/{total} \nFailed: {error}".format(success=self.count, total=self.total,
                                                                              error=self.error))
        if self.error + self.count >= self.total:
            self.finished_popup = GenericConfirmPopup("Write metadata", "Done", print)
            self.finished_popup.show()
            self.close()


class ImageChooserPopup(QWidget):
    def __init__(self, callback, id):
        super(ImageChooserPopup, self).__init__()

        self.callback = callback
        self.id = id

        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())

        if "download-path" in tracks[self.id]:
            path = QFileDialog.getOpenFileName(self, "Choose an image file", filter="JPEG files (*.jpeg *.jpg)")[0]
            if path:
                file_path = tracks[self.id]["download-path"]
                MetadataHelper(file_path).add_image_from_file(path)
                self.callback(self.id)
        else:
            self.warning = GenericConfirmPopup("Error", "Song must be downloaded before adding image", print)
            self.warning.show()
        self.close()


class Mp3ChooserPopup(QWidget):
    def __init__(self, callback, id):
        super(Mp3ChooserPopup, self).__init__()

        self.callback = callback
        self.id = id

        f = FileHelper("../../data.json")
        tracks = json.loads(f.read())
        path = QFileDialog.getOpenFileName(self, "Choose an mp3 file", filter="MP3 files (*.mp3);;FLAC files (*.flac);;All files (*.*)")[0]
        if path:
            tracks[self.id]["download-path"] = path
            js = json.dumps(tracks)
            f.overwrite(js)
            self.callback(self.id)
        self.close()


# Settings Menu
class SettingsMenu(QWidget):
    def __init__(self):
        super(SettingsMenu, self).__init__()

        self.setMinimumWidth(600)

        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QVBoxLayout()

        self.settings_manager = settings
        self.settings = self.settings_manager.settings

        from copy import deepcopy
        self.settings_fields = deepcopy(self.settings)  # A dictionary holding input field for each setting

        for setting in self.settings:
            setting_row = QHBoxLayout()
            setting_label = QLabel(_("settings_" + setting))

            setting_value = self.settings[setting]
            input_field = QLineEdit()
            if type(setting_value) is bool:
                input_field = QCheckBox()
                input_field.setChecked(setting_value)
            else:
                input_field.setMaximumWidth(50)
                input_field.setText(str(setting_value))
            self.settings_fields[setting] = input_field

            setting_row.addWidget(setting_label)
            setting_row.addStretch()
            setting_row.addWidget(input_field)

            self.view.addLayout(setting_row)

        self.button_row = QHBoxLayout()
        self.button_row.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save)
        self.button_row.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.button_row.addWidget(self.cancel_button)

        self.view.addLayout(self.button_row)

        self.setLayout(self.view)

    def on_save(self):
        for field in self.settings_fields:
            input_field = self.settings_fields[field]
            if type(input_field) is QCheckBox:
                self.settings[field] = input_field.isChecked()
            else:
                print(type(self.settings[field]))
                if type(self.settings[field]) is int:
                    try:
                        self.settings[field] = int(input_field.text())
                    except:
                        self.error_popup = GenericConfirmPopup("Error",
                                                               "{field} only accept integer".format(field=field),
                                                               print, "Non int input was found")
                        self.error_popup.show()
                else:
                    self.settings[field] = str(input_field.text())

        self.notice = GenericConfirmPopup("Notice", "Some settings may require an application restart to be effective!", print, "Notice")
        self.notice.show()
        self.settings_manager.update()
        self.close()


class GenericPathChooser(QWidget):
    def __init__(self, title, label):
        super(GenericPathChooser, self).__init__()

        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QFormLayout()

        self.but_row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.choose_path_but = QPushButton("...")
        self.but_row.addWidget(self.path_edit)
        self.but_row.addWidget(self.choose_path_but)
        self.view.addRow(label, self.but_row)

        self.confirm_but = QPushButton("Confirm")
        self.view.addWidget(self.confirm_but)

        self.setLayout(self.view)

        self.choose_path_but.clicked.connect(self.on_path_click)
        self.confirm_but.clicked.connect(self.on_confirm)

    def update_params(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def on_path_click(self):
        self.path = QFileDialog.getExistingDirectory(self, "Select a folder")
        if self.path:
            self.path_edit.setText(self.path)
            self.path_edit.setCursorPosition(0)

    def on_confirm(self):
        self.kwargs["path"] = self.path_edit.text()
        self.popup = self.fn(*self.args, **self.kwargs)
        self.popup.show()
        self.close()


class GenericConfirmPopup(QWidget):
    def __init__(self, title, label, fn, *args, **kwargs):
        super(GenericConfirmPopup, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QVBoxLayout()

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumWidth(300)
        self.label.setWordWrap(True)
        self.view.addWidget(self.label)

        self.button_row = QHBoxLayout()

        self.confirm = QPushButton("OK")
        self.confirm.clicked.connect(self.on_click)
        self.button_row.addStretch()
        self.button_row.addWidget(self.confirm)
        self.button_row.addStretch()

        self.view.addLayout(self.button_row)

        self.setLayout(self.view)

    def on_click(self):
        self.fn(*self.args, **self.kwargs)
        self.close()


class GenericTextPopup(QWidget):
    def __init__(self, title, label):
        super(GenericTextPopup, self).__init__()

        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)

        self.view = QVBoxLayout()
        self.view.setAlignment(Qt.AlignCenter)

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumWidth(300)
        self.label.setWordWrap(True)
        self.view.addWidget(self.label)

        self.setLayout(self.view)

    def set_text(self, progress):
        self.label.setText(progress)
