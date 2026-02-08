from typing import Optional
from app.framework.pubsub import Publisher
from app.schemas.feeding_event import FeedingEventSchema


class AppStateService:
    TOPIC_ROOT = "app_state"
    TOPIC_SELECTED_JAR_NAME = f"{TOPIC_ROOT}/selected_jar_name"
    TOPIC_SELECTED_FEEDING_EVENT = f"{TOPIC_ROOT}/selected_feeding_event"

    def __init__(self) -> None:
        self._selected_jar_name: Optional[str] = None
        self._selected_feeding_event: Optional[FeedingEventSchema] = None

    @property
    def selected_jar_name(self) -> Optional[str]:
        return self._selected_jar_name

    @selected_jar_name.setter
    def selected_jar_name(self, value: Optional[str]) -> None:
        if self._selected_jar_name != value:
            self._selected_jar_name = value
            Publisher.publish(value, topic=self.TOPIC_SELECTED_JAR_NAME)

    @property
    def selected_feeding_event(self) -> Optional[FeedingEventSchema]:
        return self._selected_feeding_event

    @selected_feeding_event.setter
    def selected_feeding_event(self, value: Optional[FeedingEventSchema]) -> None:
        if self._selected_feeding_event != value:
            self._selected_feeding_event = value
            Publisher.publish(value, topic=self.TOPIC_SELECTED_FEEDING_EVENT)
