from typing import Any, Optional
from app.services.log import log
from app.services.container import ContainerService
from app.views.base import BaseView
from lib.gui.core.ugui import Screen, ssd

logger = log.LogServiceManager.get_logger(name=__name__)


class Navigable:
    def on_navigated_to(self, **kwargs) -> None:
        pass

    def on_navigated_from(self) -> None:
        pass


class NavigationService:
    previous_view_ins: Optional[Navigable] = None
    current_view_ins: Optional[Navigable] = None

    @classmethod
    def navigate_to(cls, view_class: type, **kwargs) -> None:
        if not issubclass(view_class, Navigable):
            logger.error(f"View class {view_class.__name__} is not Navigable")
            return

        current_view_inst = ContainerService.get_instance(view_class)
        if not current_view_inst:
            logger.error(f"View instance doesn't exist for class {view_class.__name__}")
            return

        if cls.current_view_ins is not None:
            cls.current_view_ins.on_navigated_from()

        cls.previous_view_ins = cls.current_view_ins
        cls.current_view_ins = current_view_inst
        cls.current_view_ins.on_navigated_to(**kwargs)  # type: ignore
        Screen.change(cls.current_view_ins, mode=0)

    @classmethod
    def navigate_back(cls):
        if cls.previous_view_ins is None:
            logger.warning("No previous view to navigate back to")
            return

        previous_view_ins = cls.previous_view_ins
        cls.previous_view_ins = cls.current_view_ins
        cls.current_view_ins = previous_view_ins
        Screen.change(previous_view_ins, mode=0)
