from app.services import log
from app.services.navigation import Navigable, NavigationService
from app.views.base import BaseView
from typing import Any

from lib.gui.core.ugui import Widget, ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10
from lib.gui.widgets.buttons import Button

logger = log.LogServiceManager.get_logger(name=__name__)


class SettingsView(BaseView, Navigable):
    def __init__(self):
        super().__init__(None)
        self._writer = Writer(ssd, arial10, verbose=False)
        self._create_controls()

    def _create_controls(self) -> None:
        btn_width = int(ssd.width / 1.5)
        btn_height = self._writer.height + 4
        row = ssd.height // 2 - btn_height - 2
        col = ssd.width // 2 - btn_width // 2
        Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Reset Settings",
            callback=self._reset_settings,
        )

        row = ssd.height // 2 + 2
        Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Back",
            callback=self._navigate_back,
            args=(None,),
        )

    def _reset_settings(self, widget: Widget):
        self._notify_value_changed(reset=True)
        NavigationService.navigate_back()

    def _navigate_back(self, widget: Widget, arg: Any) -> None:
        NavigationService.navigate_back()

    def on_navigated_from(self) -> None:
        logger.debug("Navigated from SettingsView")

    def on_navigated_to(self) -> None:
        logger.debug("Navigated to SettingsView")
