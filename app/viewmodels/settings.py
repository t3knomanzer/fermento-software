import os
from typing import Any
from app.services import log
from app.viewmodels.base import BaseViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class SettingsViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()

    def on_view_value_changed(self, **kwargs) -> None:
        logger.debug(f"View value changed: {kwargs}")

        if kwargs.get("id") == "reset":
            self._reset_settings()

    def _reset_settings(self):
        logger.info("Reset settings...")
        try:
            os.remove("wifi.dat")
        except OSError as e:
            logger.error(f"Delete failed: {e}")
