import traceback, sys

from PyQt5.QtCore import *

from src.utils.Signals import WorkerSignal, ControlSignal

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Worker(QObject):
    def __init__(self, parent, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.info_signal = WorkerSignal()

        self.kwargs['progress_callback'] = self.info_signal.progress

    def run(self):
        logger.debug("Worker started")
        try:
            self.res = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.info_signal.error.emit((exctype, value, traceback.format_exc()))
            logger.error("%s %s %s", exctype, value, traceback.format_exc())
        else:
            self.info_signal.result.emit(self.res)
        finally:
            self.info_signal.finished.emit()
            return



