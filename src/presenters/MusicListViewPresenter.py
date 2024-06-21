from src.presenters.CommonPresenter import Presenter
from src.utils.Signals import EventSignal, ControlSignal

class MusicListViewPresenter(Presenter):
    def __init__(self, view):
        self.view = view
        self.control_signal = ControlSignal()


    def on_view_ready(self):
        data = {
            "0": {
                "name": "Wildest Dream",
                "artist": "Taylor Swift",
                "img_data": None
            }
        }
        self.control_signal.update.emit(data)

    def on_view_result(self, data):
        pass

    def on_view_reject(self):
        pass
