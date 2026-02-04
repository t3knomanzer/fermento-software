import asyncio
from typing import TYPE_CHECKING, Any, Optional
from lib.gui.core.ugui import Screen, Widget
from lib.gui.widgets.label import Label

if TYPE_CHECKING:
    from app.viewmodels.base import BaseViewmodel


class BaseView(Screen):
    def __init__(self, writer):
        super().__init__(writer)
        self._viewmodel: Optional["BaseViewmodel"] = None

    @property
    def viewmodel(self) -> Optional["BaseViewmodel"]:
        return self._viewmodel

    def bind_viewmodel(self, viewmodel: "BaseViewmodel") -> None:
        self._viewmodel = viewmodel

    def on_navigated_from(self):
        raise NotImplementedError("Subclasses must implement on_navigated_from method")

    def on_navigated_to(self):
        raise NotImplementedError("Subclasses must implement on_navigated_to method")

    def on_property_changed(self, property_name: str, property_value: Any):
        raise NotImplementedError(
            "Subclasses must implement on_property_changed method"
        )

    def _notify_control_changed(self, id: str, arg: Any) -> None:
        if self._viewmodel:
            self._viewmodel.on_control_changed(id, arg)

    def _set_value(self, control: Widget, value: Any) -> None:
        control.value(value)
