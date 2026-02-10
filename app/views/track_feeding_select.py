from app.framework.observer import Observable, Observer
from app.services import log
from app.services.navigation import NavigationService
from app.views.base import BaseView
from typing import Any, cast

from app.views.track_fermentation import TrackFermentationView
import config
from lib.gui.core.ugui import Widget, ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10
from lib.gui.widgets.buttons import Button
from lib.gui.widgets.label import Label

logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFeedingSelectView(BaseView):
    def __init__(self):
        super().__init__(None)

        self._writer = Writer(ssd, arial10, verbose=False)
        self._choice_btns: list[Button] = []
        self._choices: list[str] = []
        self._create_controls()

    def _create_controls(self) -> None:
        # Title label
        row = 6
        col = 0
        lbl = Label(
            self._writer,
            row=row,
            col=col,
            text=ssd.width,
            justify=Label.CENTRE,
        )
        lbl.value("Select a feeding")

        # Feeding buttons
        width = ssd.width - 8
        height = self._writer.height + 8
        row = row + self._writer.height + 6
        col = 12

        for i in range(2):
            btn = Button(self._writer, row=row, col=col, width=width, height=height, text="")
            row += height + 2
            self._choice_btns.append(btn)

    def _choose_callback(self, widget: Widget, arg: Any) -> None:
        logger.info(f"Name selected: {arg}")
        self._notify_value_changed(choice=arg)
        NavigationService.navigate_to(TrackFermentationView)

    def _update_buttons(self):
        logger.debug(f"Updating buttons with choices...")

        if len(self._choices) < config.TRACK_MAX_CHOICES:
            for i in range(len(self._choices), len(self._choice_btns)):
                logger.debug(f"Hiding button {i} as there are only {len(self._choices)} choices")
                self._choice_btns[i].visible = False  # Hide unused buttons
                self._choice_btns[i].show()  # redraw to apply visibility change

        for i, name in enumerate(self._choices):
            self._choice_btns[i].text = name  # type: ignore
            self._choice_btns[i].callback = self._choose_callback
            self._choice_btns[i].callback_args = (name,)
            self._choice_btns[i].show()

    def on_viewmodel_value_changed(self, **kwargs):
        logger.debug(f"Viewmodel value changed: {kwargs}")

        choices = kwargs.get("choices", None)
        if choices:
            self._choices = choices
            self._update_buttons()

    def on_navigated_from(self) -> None:
        logger.debug("Navigated from TrackFeedingSelectView")

    def on_navigated_to(self) -> None:
        logger.debug("Navigated to TrackFeedingSelectView")
        self._notify_value_changed(state="active")
