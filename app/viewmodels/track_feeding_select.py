import json
from lib.fermento_embedded_schemas.feeding_event import FeedingEventSchema
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from typing import Optional


logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFeedingSelectViewmodel(BaseViewmodel):
    TOPIC_ROOT = "track_feeding_event_select"
    TOPIC_CHOICE_SELECTED = f"{TOPIC_ROOT}/choice_selected"

    def __init__(self):
        super().__init__()
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)
        self._mqtt_service.subscribe_topic(topic="fermento/feeding_events/receive", qos=1)
        self._mqtt_service.add_message_handler(self.on_mqtt_message_received)

        self._choices: dict[str, FeedingEventSchema] = {}

    def _request_feeding_data(self):
        logger.info("Requesting feeding data...")
        self._mqtt_service.publish(topic=f"feeding_events/request", message="", qos=1)

    def on_view_value_changed(self, **kwargs) -> None:
        if kwargs.get("state") == "active":
            logger.info("Received status active")
            self._request_feeding_data()

        if kwargs.get("choice"):
            choice = kwargs["choice"]
            logger.info(f"Received selected choice: {choice}")
            feeding_event: Optional[FeedingEventSchema] = self._choices.get(choice, None)
            logger.info(f"Selected feeding event: {feeding_event}")
            self._app_state_service.selected_feeding_event = feeding_event

    def on_mqtt_message_received(self, message, topic):
        if topic == "fermento/feeding_events/receive":
            message = json.loads(message)
            if not isinstance(message, list):
                logger.warning(f"Unexpected message format for feeding events: {message}")
                return

            for item in message[:2]:  # Limit to first 2 events
                logger.debug(f"Processing feeding event item: {item}")
                event: FeedingEventSchema = FeedingEventSchema.from_dict(item)  # type: ignore
                ts = event.timestamp
                label = f"{ts.day}/{ts.month}/{ts.year} {ts.hour}:{ts.minute}"
                self._choices[f"{label}"] = event  # Store event with timestamp as key

            self._notify_value_changed(choices=self._choices.keys())
