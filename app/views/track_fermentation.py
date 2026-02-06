from app.services import log
from app.views.base import BaseView

from lib.gui.core.ugui import ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.freesans20 as large_font
import lib.gui.fonts.arial10 as small_font
from lib.gui.widgets.buttons import Button
from lib.gui.widgets.label import Label
import asyncio
from typing_extensions import Optional

logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFermentationView(BaseView):
    def __init__(self):
        super().__init__(None)
        self._time_update_task: Optional[asyncio.Task] = None
        self._large_writer = Writer(ssd, large_font, verbose=False)
        self._small_writer = Writer(ssd, small_font, verbose=False)
        self._create_controls()

    def _create_controls(self) -> None:
        # Bottom left (temperature)
        row = ssd.height - self._small_writer.height - 2
        width = ssd.width // 3
        self._temperature_lbl = Label(
            self._small_writer, row=row, col=2, text=width, justify=Label.LEFT
        )
        self._temperature_lbl.value("0C")

        # Bottom center (distance)
        col = ssd.width // 3
        self._distance_lbl = Label(
            self._small_writer, row=row, col=col, text=width, justify=Label.CENTRE
        )
        self._distance_lbl.value("0mm")
        # self._co2_lbl = Label(
        #     self._small_writer, row=row, col=col, text=width, justify=Label.CENTRE
        # )
        # self._co2_lbl.value("0ppm")

        # Bottom right (humidity)
        col = ssd.width // 3 * 2
        self._rh_lbl = Label(self._small_writer, row=row, col=col, text=width, justify=Label.RIGHT)
        self._rh_lbl.value("0%")

        # Center left (growth)
        width = ssd.width // 2
        row = ssd.height // 2 - self._large_writer.height // 2
        self._growth_lbl = Label(self._large_writer, row=row, col=0, text=width, justify=Label.LEFT)
        self._growth_lbl.value("0%")

        # Center right (start/stop)
        width = ssd.width // 2 - 8
        height = self._small_writer.height + 8
        col = ssd.width // 2 + 4
        self._btn = Button(
            self._small_writer,
            row=row,
            col=col,
            text="Start",
            width=width,
            height=height,
            callback=self.start_stop_callback,
        )

        # Top left (starter name)
        width = ssd.width // 3
        row = 2
        self._starter_lbl = Label(
            self._small_writer, row=row, col=2, text=width, justify=Label.LEFT
        )
        self._starter_lbl.value("Starter")

        # Top center  (time elapsed)
        col = ssd.width // 3
        self._time_lbl = Label(
            self._small_writer, row=row, col=col, text=width, justify=Label.CENTRE
        )
        self._time_lbl.value("00:00:00")

        # Top right (jar name)
        col = ssd.width // 3 * 2
        self._jar_lbl = Label(self._small_writer, row=row, col=col, text=width, justify=Label.RIGHT)
        self._jar_lbl.value("Jar")

    def on_viewmodel_value_changed(self, **kwargs):
        distance = kwargs.get("distance", None)
        if distance is not None:
            self._set_control_value(self._distance_lbl, str(distance))

        trh = kwargs.get("trh", None)
        if trh is not None:
            temperature = trh.get("t", 0.0)
            humidity = trh.get("rh", 0.0)
            self._set_control_value(self._temperature_lbl, f"{temperature:.1f}C")
            self._set_control_value(self._rh_lbl, f"{humidity:.1f}%")

    def on_navigated_from(self) -> None:
        logger.debug("Navigated from MeasureDistanceView")
        self._notify_value_changed(state="inactive")

    def on_navigated_to(self) -> None:
        logger.debug("Navigated to MeasureDistanceView")
        self._notify_value_changed(state="active")

    def start_stop_callback(self, btn: Button) -> None:
        if btn.text == "Start":
            btn.text = "Stop"  # type: ignore
            self._time_update_task = asyncio.create_task(self.update_time())

        elif btn.text == "Stop":
            btn.text = "Start"  # type: ignore
            if self._time_update_task:
                self._time_update_task.cancel()

    async def update_time(self):
        elapsed_seconds = 0
        while True:
            elapsed_seconds += 1
            h, rem = divmod(elapsed_seconds, 3600)
            m, s = divmod(rem, 60)
            self._time_lbl.value(f"{h:02d}:{m:02d}:{s:02d}")
            await asyncio.sleep(1)
