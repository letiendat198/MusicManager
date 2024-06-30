from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class EventSignal(QObject): # Presenter subscribe to this to receive user event
    ready = pyqtSignal()
    clicked = pyqtSignal(object)
    result = pyqtSignal(object)
    reject = pyqtSignal(object)
    accept = pyqtSignal(object)

class ControlSignal(QObject): # View subscribe to this to receive Presenter command
    update = pyqtSignal(object)
    close = pyqtSignal(object)
    run = pyqtSignal(object)

class WorkerSignal(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(object)
    progress = pyqtSignal(object)



