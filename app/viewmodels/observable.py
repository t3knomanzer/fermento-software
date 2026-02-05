from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.views.base import BaseView


class BaseViewmodel:
    def __init__(self):
        self._views = []

    @property
    def views(self):
        return self._views

    def bind_view(self, view: "BaseView") -> None:
        self._views.append(view)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def _notify_property_changed(self, property_name: str, property_value: Any) -> None:
        print("Notify property changed...")
        for view in self._views:
            print("Notifying view...")
            view.on_property_changed(property_name, property_value)

    def on_control_changed(self, id: str, arg: Any) -> None:
        pass

    def on_state_changed(self, state: str) -> None:
        pass
