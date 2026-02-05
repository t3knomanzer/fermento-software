from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.views.base import BaseView


class BaseViewmodel:
    def __init__(self):
        self._views: list["BaseView"] = []

    @property
    def views(self):
        return self._views

    def bind_view(self, view: "BaseView") -> None:
        self._views.append(view)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def on_view_value_changed(self, **kwargs) -> None:
        pass

    def _notify_value_changed(self, **kwargs) -> None:
        for view in self._views:
            view.on_viewmodel_value_changed(**kwargs)
