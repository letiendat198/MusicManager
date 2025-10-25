from src.presenters.CommonPresenter import Presenter
from src.utils.Signals import ControlSignal
import src.thread_manager.ThreadManager as ThreadManager
from src.utils.DatabaseHelper import DatabaseHelper, TrackObj


class InfoViewPresenter(Presenter):
    def __init__(self, view):
        super().__init__(view)

        self.view = view
        self.control_signal = ControlSignal()
        self.mediator = None


    def on_view_ready(self):
        pass

    def on_view_reject(self):
        pass

    def on_view_result(self, data):
        pass

    def on_track_update(self, id):
        thread_manager = ThreadManager.get_manager_instance()
        task_id = thread_manager.add_task(self.query_track_inf, id)
        worker_signal = thread_manager.get_worker_signal(task_id)
        worker_signal.result.connect(self.on_db_query_result)
        thread_manager.start_task(task_id)

    def query_track_inf(self, id, progress_callback = None): # Another Thread
        db = DatabaseHelper()
        track_inf = db.get_inf_by_id(id)
        track_obj = TrackObj(
            song_id=id,
            song_name=track_inf["song_name"],
            song_artists=track_inf["song_artist"],
            album_name=track_inf["album_name"],
            track_order=track_inf["track_order"],
            album_img_path=track_inf["img_path"]
        )
        return track_obj

    def on_db_query_result(self, track_obj):
        self.control_signal.update.emit(track_obj)



