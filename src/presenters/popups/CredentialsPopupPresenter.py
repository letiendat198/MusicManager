from src.presenters.CommonPresenter import Presenter
from src.utils.FileHelper import *
from src.utils.Signals import *

from typing_extensions import override

import json

class CredentialsPopupPresenter(Presenter):
    def __init__(self, view):
        super().__init__(view)

        self.control_signal = ControlSignal()

    @override
    def on_view_ready(self):
        f = FileHelper("secrets.json")
        self.control_signal.update.emit(json.loads(f.read()))
    def on_view_result(self):
        pass

    def on_view_reject(self):
        pass
