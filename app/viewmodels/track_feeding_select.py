import json
from lib.fermento_embedded_schemas.feeding_event import FeedingEventSchema
from app.services.log import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from typing import Optional

from app.utils import time


logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFeedingSelectViewmodel(BaseViewmodel):
    TOPIC_ROOT = "track_feeding_event_select"
    TOPIC_CHOICE_SELECTED = f"{TOPIC_ROOT}/choice_selected"

    def __init__(self):
        super().__init__()
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)
        self._mqtt_service.add_message_received_handler(self.on_mqtt_message_received)

        self._choices: dict[str, FeedingEventSchema] = {}

    def _request_feeding_data(self):
        logger.info("Requesting feeding data...")
        self._mqtt_service.publish(topic=f"feeding_events/request", qos=1)

    def on_view_value_changed(self, **kwargs) -> None:
        logger.debug(f"View value changed: {kwargs}")

        if kwargs.get("state") == "active":
            self._request_feeding_data()

        if kwargs.get("choice"):
            choice = kwargs["choice"]
            feeding_event: Optional[FeedingEventSchema] = self._choices.get(choice, None)

            logger.debug(f"Selected feeding event: {feeding_event}")
            self._app_state_service.selected_feeding_event = feeding_event

    def on_mqtt_message_received(self, message, topic):
        logger.debug(f"MQTT message received on topic '{topic}': {message}")

        if topic == "fermento/feeding_events/receive":
            message = json.loads(message)
            if not isinstance(message, list):
                logger.warning(f"Unexpected message format for feeding events: {message}")
                return

            message = sorted(
                message, key=lambda x: x.get("timestamp", 0), reverse=True
            )  # Sort by timestamp descending
            for item in message[:2]:  # Limit to first 2 events
                event: FeedingEventSchema = FeedingEventSchema.from_dict(item)  # type: ignore
                label = time.isoformat_to_shortform(event.timestamp)
                self._choices[f"{label}"] = event  # Store event with timestamp as key

            self._notify_value_changed(choices=self._choices.keys())
