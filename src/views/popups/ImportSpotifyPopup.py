from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import src.thread_manager.ThreadManager
from src.presenters.popups.ImportSpotifyPopupPresenter import ImportSpotifyPopupPresenter
from src.views.popups.CredentialsPopup import *
from src.utils.Signals import EventSignal

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

class ImportSpotifyPopup(QProgressDialog):
    # QProgressDialog init code have an internal show call => Will show up without being called
    def __init__(self):
        super(ImportSpotifyPopup, self).__init__()

        self.cancel() # Immediately cancel the internal show call. Weird behavior tbh

        self.event_signal = EventSignal()
        self.presenter = ImportSpotifyPopupPresenter(self)
        self.presenter.control_signal.update.connect(self.on_update)
        self.presenter.control_signal.close.connect(self.on_command_close)

        self.credential_popup = CredentialsPopup()
        self.credential_popup.event_signal.result.connect(self.on_result)
        self.credential_popup.event_signal.reject.connect(self.on_reject)
        self.credential_popup.exec_()  # Must do execute after signal connection for signal to work

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Importing from Spotify...")
        self.setMinimumWidth(350)

        self.setMaximum(0)
        self.setMinimum(0)

        self.setLabelText("Gathering information...")

        self.event_signal.ready.emit()

    def on_result(self, secret):
        logger.debug("Credentials result")
        self.event_signal.result.emit(secret)
        self.exec_()
        self.initUI()
    def on_reject(self):
        logger.debug("Credentials reject")
        self.event_signal.reject.emit()
        self.close()

    def on_update(self, data):
        logger.debug("Update issued by presenter")
        text = data["text"]
        minimum = data["min"]
        maximum = data["max"]
        value = data["value"]
        if maximum != self.maximum() or minimum != self.minimum():
            self.setMaximum(maximum)
            self.setMinimum(minimum)
        self.setValue(value)
        self.setLabelText(text)

    def on_command_close(self, data):
        self.close()
        if data is not None:
            text_popup = QMessageBox(self)
            text_popup.setText("Imported {} songs from Spotify's Liked Songs".format(str(data)))
            text_popup.setWindowTitle("Result")
            text_popup.setDefaultButton(QMessageBox.Ok)
            text_popup.exec()



