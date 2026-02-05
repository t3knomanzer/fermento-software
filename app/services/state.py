from typing import Optional
from app.framework.pubsub import Publisher


class AppStateService:
    TOPIC_ROOT = "app_state"
    TOPIC_SELECTED_NAME = f"{TOPIC_ROOT}/selected_name"

    def __init__(self) -> None:
        self._selected_name: Optional[str] = None

    @property
    def selected_name(self) -> Optional[str]:
        return self._selected_name

    @selected_name.setter
    def selected_name(self, value: Optional[str]) -> None:
        if self._selected_name != value:
            self._selected_name = value
            Publisher.publish(value, topic=self.TOPIC_SELECTED_NAME)
