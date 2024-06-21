import logging

from src.presenters.CommonPresenter import  Presenter
from src.services.SpotifyHandler import SpotifyHandler
from src.utils.Signals import ControlSignal
from src.utils.ThreadWorker import Worker

import src.common.ThreadPool as ThreadPool

logger = logging.getLogger(__name__)
class ImportSpotifyPopupPresenter(Presenter):
    def __init__(self, view):
        super().__init__(view)

        self.control_signal = ControlSignal()

    def on_view_ready(self):
        logger.debug("View ready")

    def on_view_result(self, secret):
        logger.debug("View is passing result")
        self.spotify_handler = SpotifyHandler(secret["client_id"], secret["client_secret"])
        self.worker = Worker(self.spotify_handler.get_liked_track)
        self.worker.signal.progress.connect(self.on_worker_update)
        self.worker.signal.finished.connect(self.on_worker_finished)
        ThreadPool.threadpool.start(self.worker)

    def on_view_reject(self):
        pass

    def on_worker_update(self, prog):
        data = {
            "text": "Found {} songs".format(prog),
            "min": 0,
            "max": 0,
            "value": 0
        }
        self.control_signal.update.emit(data)

    def on_worker_finished(self):
        self.control_signal.close.emit()