from app.services import log
from app.viewmodels.base import BaseViewmodel
from lib.pubsub.pubsub import Publisher, Subscriber

logger = log.LogServiceManager.get_logger(name=__name__)


class SplashViewmodel(BaseViewmodel, Subscriber):
    def __init__(self):
        super().__init__()
        Publisher.subscribe(self, "splash_message")
        self._splash_message = ""

    @property
    def splash_message(self) -> str:
        return self._splash_message

    @splash_message.setter
    def splash_message(self, value: str) -> None:
        if self._splash_message != value:
            self._splash_message = value
            self._notify_property_changed("splash_message", value)

    def on_message_received(self, message, topic):
        if topic == "splash_message":
            self.splash_message = message
