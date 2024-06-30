import logging

from src.presenters.CommonPresenter import  Presenter
from src.services.SpotifyHandler import SpotifyHandler
from src.utils.Signals import ControlSignal
from src.thread_manager.ThreadWorker import Worker

import src.thread_manager.ThreadManager as ThreadManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
class ImportSpotifyPopupPresenter(Presenter):
    def __init__(self, view):
        super().__init__(view)

        self.control_signal = ControlSignal()
        self.result = 0

    def on_view_ready(self):
        logger.debug("View ready")

    def on_view_result(self, secret):
        logger.debug("View is passing result")
        self.model(secret)
        # Not really a model. Just a separation!
        # It's too short for a separate Model class with its separate set of signals
        # So we have this monstrosity in Presenter

    def model(self, secret):
        self.spotify_handler = SpotifyHandler(secret["client_id"], secret["client_secret"])
        thread_manager = ThreadManager.get_manager_instance()
        task_id = thread_manager.add_task(self.spotify_handler.get_liked_track)
        worker_signal = thread_manager.get_worker_signal(task_id)
        worker_signal.progress.connect(self.on_worker_update)
        worker_signal.finished.connect(self.on_worker_finished)
        worker_signal.error.connect(self.on_worker_error)
        thread_manager.start_task(task_id)

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
        self.result = prog

    def on_worker_finished(self):
        self.control_signal.close.emit(self.result)

    def on_worker_error(self, exc):
        pass