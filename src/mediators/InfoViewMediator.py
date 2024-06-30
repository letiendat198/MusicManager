from src.mediators.Mediator import Mediator
from src.presenters.CommonPresenter import Presenter
from typing_extensions import override


class InfoViewMediator(Mediator):
    def __init__(self, guest_presenter, infoview_presenter):
        self.infoview_presenter = infoview_presenter
        self.infoview_presenter.mediator = self
        self.guest_presenter = guest_presenter
        self.guest_presenter.mediator = self

    @override
    def notify(self, sender: Presenter, event: str) -> None:
        pass




