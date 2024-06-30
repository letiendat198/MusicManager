from abc import ABC, abstractmethod

from src.presenters.CommonPresenter import Presenter



class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: Presenter, event: str) -> None:
        pass
