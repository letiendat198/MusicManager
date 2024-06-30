from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QWidget

from src.thread_manager.ThreadWorker import Worker

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
class _ThreadManager(QObject): # Not meant to be inited anywhere else
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.worker_queue = {}
        self.threadpool = {}
        self.thread_queue = []
        self.current_id = 0
        self.max_thread_count = 12
        logger.debug("Thread Manager initiated with %d threads",self.max_thread_count)

    def add_task(self, fn, *args, **kwargs): # Queue a task
        self.current_id += 1
        worker = Worker(self, fn, *args, **kwargs)
        self.worker_queue[self.current_id] = worker

        logger.debug("Created a task with id: %d", self.current_id)
        return self.current_id

    def start_task(self, id):
        #Check if threadpool exceed max_thread_count
        if len(self.threadpool) >= self.max_thread_count:
            # Push the worker from worker_queue to thread_queue
            self.thread_queue.append(id)

            logger.debug("Threadpool limit exceeded. Queueing task id: %d", id)
            return

        # Add thread to the managed threadpool
        self.thread = QThread(self) # Need to be self or have a parent to survive
        self.threadpool[id] = self.thread

        self.worker = self.worker_queue[id]
        self.worker_queue.pop(id)
        
        self.worker.moveToThread(self.thread)
        self.worker.info_signal.finished.connect(self.thread.quit)
        self.thread.finished.connect(lambda: self.on_thread_finished(id))
        self.thread.started.connect(self.worker.run)

        self.thread.start()
        logger.debug("Starting a thread for task id: %d", id)


    def cancel_task(self, id):
        if id in self.threadpool:
            thread = self.threadpool[id]
            thread.quit()
        elif id in self.thread_queue:
            self.thread_queue.remove(id)

    def start_queued_thread(self):
        if len(self.thread_queue)!=0 and len(self.threadpool)<self.max_thread_count:
            queued_id = self.thread_queue[0]
            self.thread_queue.pop(0)

            logger.debug("Starting a queued thread with id: %d", queued_id)
            self.start_task(queued_id)

    def get_worker_signal(self, id):
        return self.worker_queue[id].info_signal

    def on_thread_finished(self, id):
        logger.debug("Thread id %d returned, cleaning up", id)
        thread = self.threadpool[id]
        thread.deleteLater()
        self.threadpool.pop(id)

        self.start_queued_thread()
        logger.debug("Cleaned up thread %d. Current threadpool: %d, current thread queue: %d", id, len(self.threadpool), len(self.thread_queue))

    def set_max_thread_count(self, count):
        self.max_thread_count = count

thread_manager = _ThreadManager()
def get_manager_instance():
    return thread_manager





