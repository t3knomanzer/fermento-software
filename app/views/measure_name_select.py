import config
from app.services.log import log
from app.services.navigation import Navigable, NavigationService
from app.views.base import BaseView
from typing import Any

from app.views.measure_distance import MeasureDistanceView
from lib.gui.core.ugui import Widget, ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10
from lib.gui.widgets.buttons import Button
from lib.gui.widgets.label import Label

logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureNameSelectView(BaseView, Navigable):
    def __init__(self):
        super().__init__(None)

        self._writer = Writer(ssd, arial10, verbose=False)
        self._choice_btns: list[Button] = []
        self._choices: set[str] = set()
        self._create_controls()

    def _create_controls(self) -> None:
        # Title
        margin = 6
        row = ssd.height // 2 - self._writer.height - margin
        col = 0
        lbl = Label(
            self._writer,
            row=row,
            col=0,
            text=ssd.width,
            justify=Label.CENTRE,
        )
        lbl.value("Select a name")

        # Choice buttons
        self._choice_btns.clear()
        btn_width = ssd.width // 3 - margin
        for i in range(3):
            col = (btn_width * i) + (margin * (i + 1))
            btn = Button(self._writer, row=ssd.height // 2, col=col, width=btn_width, text="")
            self._choice_btns.append(btn)

    def _choose_callback(self, widget: Widget, arg: Any) -> None:
        logger.info(f"Name selected: {arg}")
        self._notify_value_changed(choice=arg)
        NavigationService.navigate_to(MeasureDistanceView)

    def _update_buttons(self):
        logger.debug(f"Updating buttons with choices...")

        for i, name in enumerate(self._choices):
            self._choice_btns[i].text = name  # type: ignore
            self._choice_btns[i].callback = self._choose_callback
            self._choice_btns[i].callback_args = (name,)
            self._choice_btns[i].show()

    def _navigate_callback(self, button: Widget, view: type) -> None:
        NavigationService.navigate_to(view)

    def on_viewmodel_value_changed(self, **kwargs):
        logger.debug(f"Viewmodel value changed: {kwargs}")

        choices = kwargs.get("choices", None)
        if not choices or len(choices) != config.MEASURE_MAX_CHOICES:
            logger.error(f"Invalid choices received: {choices}")
            return

        self._choices = choices
        self._update_buttons()

    def on_navigated_from(self) -> None:
        logger.debug("Navigated from MeasureNameSelectView")

    def on_navigated_to(self) -> None:
        logger.debug("Navigated to MeasureNameSelectView")
        self._notify_value_changed(state="active")
