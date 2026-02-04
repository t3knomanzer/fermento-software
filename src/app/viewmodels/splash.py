
from app.viewmodels.base import BaseViewmodel
import config


class SplashViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
        self._splash_message = ""

    @property
    def splash_message(self) -> str:
        return self._splash_message

    @splash_message.setter
    def splash_message(self, value: str) -> None:
        print("Setting splash_message")
        if self._splash_message != value:
            self._splash_message = value
            self.notify_property_changed("splash_message", value)
