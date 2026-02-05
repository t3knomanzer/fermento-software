from app.services import log
from app.views.base import BaseView

from lib.gui.core.colors import BLACK, WHITE
from lib.gui.core.ugui import ssd
from lib.gui.widgets.bitmap import BitMap
from lib.gui.widgets.label import Label
from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10

logger = log.LogServiceManager.get_logger(name=__name__)


class SplashView(BaseView):
    def __init__(self):
        self._writer = Writer(ssd, arial10, verbose=False)
        super().__init__(self._writer)
        self._create_controls()

    def _create_controls(self) -> None:
        # Logo
        bmp_size = (100, 60)
        screen_center_v = ssd.height // 2 - self._writer.height // 2
        col = ssd.width // 2 - bmp_size[0] // 2
        row = ssd.height // +bmp_size[1] // 2
        self._bmp_logo = BitMap(
            self._writer,
            row,
            col,
            bmp_size[1],
            bmp_size[0],
            fgcolor=BLACK,
            bgcolor=WHITE,
            bdcolor=None,  # type: ignore
        )
        self._bmp_logo.value(path := "assets/logo.xbm")

        # Progress messages
        self._lbl_msg = Label(
            self._writer,
            screen_center_v + self._bmp_logo.height + 4,
            64,
            128,
            justify=Label.CENTRE,
        )

    def on_viewmodel_value_changed(self, **kwargs):
        message = kwargs.get("message", None)
        if message:
            logger.info(f"Setting splash_message to {message}")
            self._set_control_value(self._lbl_msg, message)

    def on_navigated_from(self) -> None:
        logger.debug(f"Navigated from SplashView")

    def on_navigated_to(self) -> None:
        logger.debug(f"Navigated to SplashView")
