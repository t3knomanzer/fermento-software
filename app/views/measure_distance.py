from app.services.log import log
from app.services.navigation import Navigable, NavigationService
from app.views.base import BaseView

from app.views.menu import MenuView
from lib.gui.core.ugui import Widget, ssd
from lib.gui.core.writer import Writer
import lib.gui.fonts.freesans20 as large_font
import lib.gui.fonts.arial10 as small_font
from lib.gui.widgets.buttons import Button
from lib.gui.widgets.label import Label

logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureDistanceView(BaseView, Navigable):
    def __init__(self):
        super().__init__(None)
        self._large_writer = Writer(ssd, large_font, verbose=False)
        self._small_writer = Writer(ssd, small_font, verbose=False)
        self._create_controls()

    def _create_controls(self) -> None:
        # Jar name
        lbl_width = ssd.width
        self._name_lbl = Label(
            self._small_writer, row=4, col=0, text=lbl_width, justify=Label.CENTRE
        )
        self._name_lbl.value("")

        # Distance
        lbl_row = ssd.height // 2 - int(self._large_writer.height / 1.5)
        self._distance_lbl = Label(
            self._large_writer, row=lbl_row, col=0, text=lbl_width, justify=Label.CENTRE
        )
        self._distance_lbl.value("0mm")

        # Save button
        btn_width = 48
        btn_margin = 4
        screen_center_h = ssd.width // 2
        btn_save = Button(
            self._small_writer,
            0,
            0,
            width=btn_width,
            text="save",
            callback=self._save_calllback,
        )

        # Cancel button
        from app.views.menu import MenuView

        btn_cancel = Button(
            self._small_writer,
            0,
            0,
            width=btn_width,
            text="cancel",
            callback=self._navigate_callback,
            args=(MenuView,),
        )
        btn_save.row = ssd.height - btn_save.height - btn_margin // 2
        btn_cancel.row = btn_save.row
        btn_save.col = screen_center_h - btn_width - btn_margin // 2
        btn_cancel.col = screen_center_h + btn_margin // 2

    def _save_calllback(self, widget: Widget):
        self._notify_value_changed(save=True)
        NavigationService.navigate_to(MenuView)

    def _navigate_callback(self, button: Widget, view: type):
        NavigationService.navigate_to(view)

    def on_viewmodel_value_changed(self, **kwargs):
        logger.debug(f"Viewmodel value changed: {kwargs}")

        distance = kwargs.get("distance", None)
        if distance is not None:
            self._set_control_value(self._distance_lbl, f"{distance}mm")

        name = kwargs.get("name", None)
        if name is not None:
            self._set_control_value(self._name_lbl, name)

    def on_navigated_from(self) -> None:
        logger.debug("Navigated from MeasureDistanceView")
        self._notify_value_changed(state="inactive")

    def on_navigated_to(self) -> None:
        logger.debug("Navigated to MeasureDistanceView")
        self._notify_value_changed(state="active")
