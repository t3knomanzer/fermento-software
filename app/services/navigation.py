from typing import Optional
from app.services.app import ApplicationService
from app.views.base import BaseView
from lib.gui.core.ugui import Screen, ssd


class NavigationService:
    previous_view_ins: Optional[BaseView] = None
    current_view_ins: Optional[BaseView] = None

    @classmethod
    def navigate_to(cls, view_class: type) -> None:
        if cls.current_view_ins is not None:
            cls.current_view_ins.on_navigated_from()

        current_view_inst = ApplicationService.get_view(view_class)
        if not current_view_inst:
            raise KeyError(
                f"View instance doesn't exist for class {view_class.__name__}"
            )

        cls.previous_view_ins = cls.current_view_ins
        cls.current_view_ins = current_view_inst
        cls.current_view_ins.on_navigated_to()
        Screen.change(cls.current_view_ins, mode=0)

    @classmethod
    def navigate_back(cls):
        previous_view_ins = cls.previous_view_ins
        cls.previous_view_ins = cls.current_view_ins
        cls.current_view_ins = previous_view_ins
        Screen.change(previous_view_ins, mode=0)
