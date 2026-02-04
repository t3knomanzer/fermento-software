from app.views.base import BaseView
from typing import Any

from lib.gui.core.ugui import ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10
from lib.gui.widgets.buttons import Button


class SettingsView(BaseView):
    def __init__(self):
        super().__init__(None)
        self._writer = Writer(ssd, arial10, verbose=False)
        self._create_controls()

    def _create_controls(self) -> None:
        pass

    def on_property_changed(self, name: str, value: Any) -> None:
        pass

    def on_navigated_from(self) -> None:
        pass

    def on_navigated_to(self) -> None:
        pass
