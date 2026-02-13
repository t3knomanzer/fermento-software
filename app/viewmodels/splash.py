from app.services.log import log
from app.viewmodels.base import BaseViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class SplashViewmodel(BaseViewmodel):
    def __init__(self):
        BaseViewmodel.__init__(self)
        self._message = ""

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        logger.debug(f"Setting splash message: {value}")
        if self._message != value:
            self._message = value
            self._notify_value_changed(message=value)
