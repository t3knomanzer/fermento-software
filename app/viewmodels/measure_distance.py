from typing import Any, Optional
from app.framework.pubsub import Publisher, Subscriber
from lib.fermento_embedded_schemas import JarSchema
from app.sensors.distance import DistanceSensor
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from app.framework.observer import Observer
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel
import json

logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureDistanceViewmodel(BaseViewmodel, Subscriber):
    def __init__(self):
        super().__init__()
        Publisher.subscribe(self, topic=DistanceSensor.TOPIC_DISTANCE)
        Publisher.subscribe(self, topic=AppStateService.TOPIC_SELECTED_JAR_NAME)

        self._name: Optional[str] = None
        self._distance: int = 0
        self._distance_sensor: DistanceSensor = ContainerService.get_instance(DistanceSensor)
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)

    def save_measurement(self) -> None:
        if self._name is None:
            logger.warning("No name selected, cannot save measurement.")
            return

        logger.info(f"Saving measurement: name={self._name}, distance={self._distance}")
        message = JarSchema(name=self._name, height=self._distance).to_dict()
        self._mqtt_service.publish(topic=f"jars/create", message=message, qos=1)

    def on_view_value_changed(self, **kwargs) -> None:
        state = kwargs.get("state", None)
        if state == "active":
            self._distance_sensor.start()

        elif state == "inactive":
            self._distance_sensor.stop()

        save = kwargs.get("save", None)
        if save:
            logger.info("Save requested, stopping sensor...")
            self._distance_sensor.stop()
            self.save_measurement()

    def on_publisher_message_received(self, message: Any, topic: str):
        if topic == DistanceSensor.TOPIC_DISTANCE:
            self._distance = message
            self._notify_value_changed(distance=message)

        elif topic == AppStateService.TOPIC_SELECTED_JAR_NAME:
            self._name = message
            self._notify_value_changed(name=message)
