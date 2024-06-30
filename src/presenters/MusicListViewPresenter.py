from src.presenters.CommonPresenter import Presenter
from src.utils.Signals import EventSignal, ControlSignal
from src.views.components.MusicEntry import MusicEntry
from src.utils.DatabaseHelper import DatabaseHelper

import src.thread_manager.ThreadManager as ThreadManager
import src.models.ResolveImageUrl as ResolveImageUrl
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MusicListViewPresenter(Presenter):
    def __init__(self, view):
        super().__init__(view)

        self.view = view
        self.control_signal = ControlSignal()

    def on_view_ready(self):
        self.thread_manager = ThreadManager.get_manager_instance()
        task_id = self.thread_manager.add_task(self.query_db_for_songs)
        worker_signal = self.thread_manager.get_worker_signal(task_id)
        worker_signal.progress.connect(self.on_db_query_progress)
        self.thread_manager.start_task(task_id)

    def on_view_result(self, data):
        pass

    def on_view_reject(self):
        pass

    def on_db_query_progress(self, data):
        if data["img_path"] is not None:
            data["img"] = data["img_path"]
        elif data["img_url"] is not None:
            self.resolve_image_url(data["img_url"], data)
        self.control_signal.update.emit(data)

    def query_db_for_songs(self, progress_callback=None): # This is on another thread
        db = DatabaseHelper()
        for song_info in db.get_all_from_playlist("playlist1"):
            data = {
                "id": song_info["platform_id"],
                "name": song_info["song_name"],
                "artist": song_info["song_artist"],
                "mode": MusicEntry.IMAGE_PATH,
                "img": "resources/placeholder.jpg",
                "img_path": song_info["img_path"],
                "img_url": song_info["img_url"],
            }
            if progress_callback is not None:
                progress_callback.emit(data)

    def resolve_image_url(self, url, data):
        task_id = self.thread_manager.add_task(ResolveImageUrl.get_data_from_url, url)
        worker_signal = self.thread_manager.get_worker_signal(task_id)
        worker_signal.result.connect(lambda res: self.on_image_resolve(res, data))
        self.thread_manager.start_task(task_id)

    def on_image_resolve(self, res, data): # TODO: Need rework, should save image data to cache
        data["mode"] = MusicEntry.IMAGE_DATA
        data["img"] = res
        self.control_signal.update.emit(data)