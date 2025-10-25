from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.utils.Signals import EventSignal
from src.presenters.popups.CredentialsPopupPresenter import CredentialsPopupPresenter

import logging

logger = logging.getLogger(__name__)
class CredentialsPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.event_signal = EventSignal()

        self.presenter = CredentialsPopupPresenter(self)
        self.presenter.control_signal.update.connect(self.on_update)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Input API Credentials")
        self.setMinimumWidth(350)

        self.view = QFormLayout(self)

        self.id_input = QLineEdit()
        self.secret_input = QLineEdit()

        self.view.addRow("Client ID:", self.id_input)
        self.view.addRow("Client Secret:", self.secret_input)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)
        self.view.addRow(self.buttonBox)

        self.setLayout(self.view)

        self.event_signal.ready.emit()

    def on_update(self, secret):
        logger.debug("Credentials Input view updated by Presenter")
        self.id_input.setText(secret["client_id"])
        self.secret_input.setText(secret["client_secret"])

    def on_accept(self):
        logger.debug("Accepted")
        self.close()
        cred = {
            "client_id": self.id_input.text(),
            "client_secret": self.secret_input.text()
        }
        self.event_signal.result.emit(cred)
    def on_reject(self):
        logger.debug("Rejected")
        self.event_signal.reject.emit("")
        self.close()
