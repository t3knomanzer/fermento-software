import json
from typing import Any, Optional
from app.schemas.feeding_event import FeedingEventSchema
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from app.resources.names import NAMES
from typing_extensions import cast


logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFeedingSelectViewmodel(BaseViewmodel):
    TOPIC_ROOT = "track_feeding_event_select"
    TOPIC_CHOICE_SELECTED = f"{TOPIC_ROOT}/choice_selected"

    def __init__(self):
        super().__init__()
        self._app_state_service: AppStateService = ContainerService.get_instance(
            AppStateService
        )
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)
        self._mqtt_service.subscribe_topic(
            topic="fermento/feeding_events/receive", qos=1
        )
        self._mqtt_service.add_message_handler(self.on_mqtt_message_received)

        self._feeding_events: list[FeedingEventSchema] = []
        self._choices: list[str] = []

    def _request_feeding_data(self):
        logger.info("Requesting feeding data...")
        self._mqtt_service.publish(topic=f"feeding_events/request", message="", qos=1)

    def on_view_value_changed(self, **kwargs) -> None:
        if kwargs.get("state") == "active":
            logger.info("Received status active")
            self._request_feeding_data()

        if kwargs.get("choice"):
            choice = kwargs["choice"]
            logger.info(f"Received picked choice: {choice}")
            self._app_state_service.selected_feeding_id = choice

    def on_mqtt_message_received(self, message, topic):
        if topic == "fermento/feeding_events/receive":
            logger.info(
                f"Received feeding events response: message type={type(message)} message={message}"
            )
            message = json.loads(message)
            if not isinstance(message, list):
                logger.warning(
                    f"Unexpected message format for feeding events: {message}"
                )
                return

            for item in message[:2]:  # Limit to first 2 events
                event: FeedingEventSchema = FeedingEventSchema.from_dict(item)  # type: ignore
                self._feeding_events.append(event)

            self._choices = [f"{event.date}" for event in self._feeding_events]
            self._notify_value_changed(choices=self._choices)
