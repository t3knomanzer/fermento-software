from typing import Any, Optional
from app.services import log
from app.services.container import ContainerService
from app.views.base import BaseView
from lib.gui.core.ugui import Screen, ssd

logger = log.LogServiceManager.get_logger(name=__name__)


class NavigationService:
    previous_view_ins: Optional[BaseView] = None
    current_view_ins: Optional[BaseView] = None

    @classmethod
    def navigate_to(cls, view_class: type, **kwargs) -> None:
        if cls.current_view_ins is not None:
            cls.current_view_ins.on_navigated_from()

        current_view_inst = ContainerService.get_instance(view_class)
        if not current_view_inst:
            logger.critical(f"View instance doesn't exist for class {view_class.__name__}")
            return

        cls.previous_view_ins = cls.current_view_ins
        cls.current_view_ins = current_view_inst
        cls.current_view_ins.on_navigated_to(**kwargs)  # type: ignore
        Screen.change(cls.current_view_ins, mode=0)

    @classmethod
    def navigate_back(cls):
        previous_view_ins = cls.previous_view_ins
        cls.previous_view_ins = cls.current_view_ins
        cls.current_view_ins = previous_view_ins
        Screen.change(previous_view_ins, mode=0)
