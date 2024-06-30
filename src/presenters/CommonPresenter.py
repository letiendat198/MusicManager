from abc import ABC, abstractmethod

from src.mediators.Mediator import Mediator


class Presenter(ABC):
    def __init__(self, view):
        self.view = view
        self.mediator: Mediator

        # Not supposed to do these here but it's convenient. May come back and screw me later
        self.view.event_signal.ready.connect(self.on_view_ready)
        self.view.event_signal.result.connect(self.on_view_result)
        self.view.event_signal.reject.connect(self.on_view_reject)

    @abstractmethod
    def on_view_ready(self):
        pass

    @abstractmethod
    def on_view_result(self, data):
        pass

    @abstractmethod
    def on_view_reject(self):
        pass