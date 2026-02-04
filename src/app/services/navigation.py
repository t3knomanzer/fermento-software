from typing import Optional
from app.services.app import ApplicationService
from app.views.base import BaseView
from lib.gui.core.ugui import Screen, ssd


class NavigationService:
    current_view_inst: Optional[BaseView] = None

    @classmethod
    def navigate_to(cls, view_class: type) -> None:
        if cls.current_view_inst is not None:
            cls.current_view_inst.on_navigated_from()

        current_view_inst = ApplicationService.get_view(view_class)
        if not current_view_inst:
            raise KeyError(
                f"View instance doesn't exist for class {view_class.__name__}"
            )

        cls.current_view_inst = current_view_inst
        cls.current_view_inst.on_navigated_to()
        Screen.change(cls.current_view_inst, mode=0)
