from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class EventSignal(QObject): # Presenter subscribe to this to receive user event
    ready = pyqtSignal()
    clicked = pyqtSignal(str)
    result = pyqtSignal(dict)
    reject = pyqtSignal()
    accept = pyqtSignal()

class ControlSignal(QObject): # View subscribe to this to receive Presenter command
    update = pyqtSignal(dict)
    close = pyqtSignal()



