from typing import Optional
from app.framework.pubsub import Publisher


class AppStateService:
    TOPIC_ROOT = "app_state"
    TOPIC_SELECTED_JAR_NAME = f"{TOPIC_ROOT}/selected_jar_name"
    TOPIC_SELECTED_FEEDING_ID = f"{TOPIC_ROOT}/selected_feeding_id"

    def __init__(self) -> None:
        self._selected_jar_name: Optional[str] = None
        self._selected_feeding_id: Optional[str] = None

    @property
    def selected_jar_name(self) -> Optional[str]:
        return self._selected_jar_name

    @selected_jar_name.setter
    def selected_jar_name(self, value: Optional[str]) -> None:
        if self._selected_jar_name != value:
            self._selected_jar_name = value
            Publisher.publish(value, topic=self.TOPIC_SELECTED_JAR_NAME)

    @property
    def selected_feeding_id(self) -> Optional[str]:
        return self._selected_feeding_id

    @selected_feeding_id.setter
    def selected_feeding_id(self, value: Optional[str]) -> None:
        if self._selected_feeding_id != value:
            self._selected_feeding_id = value
            Publisher.publish(value, topic=self.TOPIC_SELECTED_FEEDING_ID)
