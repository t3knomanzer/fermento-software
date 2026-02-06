from typing import Any, Optional
from app.framework.pubsub import Publisher, Subscriber
from app.schemas.jar import JarSchema
from app.sensors.distance import DistanceSensor
from app.sensors.trh import TRHSensor
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from app.framework.observer import Observer
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel
import json

logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFermentationViewmodel(BaseViewmodel, Subscriber):
    def __init__(self):
        super().__init__()
        Publisher.subscribe(self, topic=DistanceSensor.TOPIC_DISTANCE)
        Publisher.subscribe(self, topic=TRHSensor.TOPIC_DATA)

        self._distance: int = 0
        self._trh: dict[str, Any] = {"t": 0.0, "rh": 0.0}

        self._distance_sensor: DistanceSensor = ContainerService.get_instance(DistanceSensor)
        self._trh_sensor: TRHSensor = ContainerService.get_instance(TRHSensor)
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)

    def on_view_value_changed(self, **kwargs) -> None:
        state = kwargs.get("state", None)
        if state == "active":
            self._distance_sensor.start()
            self._trh_sensor.start()

        elif state == "inactive":
            self._distance_sensor.stop()
            self._trh_sensor.stop()

    def on_publisher_message_received(self, message: Any, topic: str):
        if topic == DistanceSensor.TOPIC_DISTANCE:
            self._distance = message
            self._notify_value_changed(distance=message)

        elif topic == TRHSensor.TOPIC_DATA:
            self._trh = message
            self._notify_value_changed(trh=message)

