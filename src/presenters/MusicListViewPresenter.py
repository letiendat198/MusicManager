import re

from src.cache_manager.CacheManager import CacheManager
from src.mediators.Mediator import MediatorEvent
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
        self.mediator = None

        self.view.event_signal.clicked.connect(self.on_view_clicked)

        self.album_image_cached = []

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

    def on_view_clicked(self, id):
        self.mediator.notify(self, MediatorEvent(MediatorEvent.UPDATE_EVENT, id))

    def on_db_query_progress(self, data):
        if data["img_path"] is not None:
            data["img"] = data["img_path"]
        elif data["img_url"] is not None:
            if data["album"] not in self.album_image_cached:
                logger.debug("Cached image not found but have url, caching")
                self.album_image_cached.append(data["album"])
                self.cache_album_image(data)
            else:
                logger.debug("Image caching for this album has already started, skipping")

        self.control_signal.update.emit(data)

    def query_db_for_songs(self, progress_callback=None): # This is on another thread
        logger.debug("Query DB for songs")
        db = DatabaseHelper()
        for song_info in db.get_all_from_playlist("playlist1"):
            data = {
                "id": song_info["platform_id"],
                "name": song_info["song_name"],
                "artist": song_info["song_artist"],
                "album": song_info["album_name"],
                "mode": MusicEntry.IMAGE_PATH,
                "img": "resources/placeholder.jpg",
                "img_path": song_info["img_path"],
                "img_url": song_info["img_url"],
            }
            if progress_callback is not None:
                progress_callback.emit(data)

    def cache_album_image(self, data):
        sanitized_file_name = re.sub('[\\/?:*"<>|]', '', data["album"])
        file_name = sanitized_file_name + ".jpg"
        cache_manager = CacheManager()
        task_id = self.thread_manager.add_task(cache_manager.cache_image_from_url, data["img_url"], file_name)
        worker_signal = self.thread_manager.get_worker_signal(task_id)
        worker_signal.result.connect(lambda path: self.on_cache_img_result(path, data))
        self.thread_manager.start_task(task_id)

    def on_cache_img_result(self, cache_path, data):
        logger.debug("Finish cache image at %s, updating view", cache_path)
        data["img"] = cache_path
        db = DatabaseHelper()
        db.update_row("albums", "album_name", data["album"], "img_path", cache_path)
        self.control_signal.update.emit(data)