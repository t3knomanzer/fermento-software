from typing import Callable, Optional
from app.services.log import log
from lib.fermento_embedded_schemas.feeding_event import FeedingEventSchema

logger = log.LogServiceManager.get_logger(name=__name__)


class AppStateService:
    def __init__(self) -> None:
        self._selected_jar_name: Optional[str] = None
        self._selected_feeding_event: Optional[FeedingEventSchema] = None
        self._selected_jar_name_handlers: list[Callable] = []
        self._selected_feeding_event_handlers: list[Callable] = []

    @property
    def selected_jar_name(self) -> Optional[str]:
        return self._selected_jar_name

    @selected_jar_name.setter
    def selected_jar_name(self, value: Optional[str]) -> None:
        if self._selected_jar_name != value:
            logger.debug(f"Updating selected_jar_name to {value}")
            self._selected_jar_name = value
            self._notify_selected_jar_name_handlers()

    @property
    def selected_feeding_event(self) -> Optional[FeedingEventSchema]:
        return self._selected_feeding_event

    @selected_feeding_event.setter
    def selected_feeding_event(self, value: Optional[FeedingEventSchema]) -> None:
        if self._selected_feeding_event != value:
            logger.debug(f"Updating selected_feeding_event to {value}")
            self._selected_feeding_event = value
            self._notify_selected_feeding_event_handlers()

    def add_selected_jar_name_handler(self, handler: Callable) -> None:
        self._selected_jar_name_handlers.append(handler)

    def add_selected_feeding_event_handler(self, handler: Callable) -> None:
        self._selected_feeding_event_handlers.append(handler)

    def _notify_selected_jar_name_handlers(self) -> None:
        for handler in self._selected_jar_name_handlers:
            handler(self._selected_jar_name)

    def _notify_selected_feeding_event_handlers(self) -> None:
        for handler in self._selected_feeding_event_handlers:
            handler(self._selected_feeding_event)
