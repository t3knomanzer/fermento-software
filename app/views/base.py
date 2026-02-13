from typing import TYPE_CHECKING, Any, Optional
from app.services.log import log
from lib.gui.core.ugui import Screen, Widget

if TYPE_CHECKING:
    from app.viewmodels.base import BaseViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class BaseView(Screen):
    def __init__(self, writer, *args, **kwargs):
        super().__init__(writer, *args, **kwargs)
        self._viewmodel: Optional["BaseViewmodel"] = None

    @property
    def viewmodel(self) -> Optional["BaseViewmodel"]:
        return self._viewmodel

    def bind_viewmodel(self, viewmodel: "BaseViewmodel") -> None:
        self._viewmodel = viewmodel

    def on_viewmodel_value_changed(self, **kwargs):
        pass

    def _notify_value_changed(self, **kwargs):
        if self._viewmodel:
            self._viewmodel.on_view_value_changed(**kwargs)

    def _set_control_value(self, control: Widget, value: Any) -> None:
        control.value(value)
