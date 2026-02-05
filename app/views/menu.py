from app.services import log
from app.services.navigation import NavigationService
from app.views.base import BaseView
from typing import Any

from lib.gui.core.ugui import Widget, ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10
from lib.gui.widgets.buttons import Button

logger = log.LogServiceManager.get_logger(name=__name__)


class MenuView(BaseView):
    def __init__(self):
        super().__init__(None)
        self._writer = Writer(ssd, arial10, verbose=False)
        self._create_controls()

    def _create_controls(self) -> None:
        # UI widgets
        btn_width = int(ssd.width / 1.5)
        btn_height = self._writer.height + 4

        # Measure button
        from app.views.measure_name_select import MeasureNameSelectView

        row = (ssd.height // 2) - btn_height // 2 - btn_height - 4
        col = ssd.width // 2 - btn_width // 2
        btn_01 = Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Measure",
            callback=self._navigate_callback,
            args=(MeasureNameSelectView,),
        )

        # Track button
        row = ssd.height // 2 - btn_height // 2
        btn_02 = Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Track",
            callback=self._navigate_callback,
            args=("Track", None),
        )

        # Settings button
        from app.views.settings import SettingsView

        row = (ssd.height // 2) + btn_height // 2 + 4
        btn_03 = Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Settings",
            callback=self._navigate_callback,
            args=(SettingsView,),
        )

    def _navigate_callback(self, button: Widget, view: type):
        NavigationService.navigate_to(view)

    def on_navigated_from(self) -> None:
        logger.debug("Navigated from MenuView")

    def on_navigated_to(self) -> None:
        logger.debug("Navigated to MenuView")
