from abc import ABC, abstractmethod

from src.presenters.CommonPresenter import Presenter

class MediatorEvent:
    UPDATE_EVENT = 1
    def __init__(self, event_type: int = None, data: object = None):
        self.event_type = event_type
        self.data = data


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: Presenter, event: MediatorEvent) -> None:
        pass



