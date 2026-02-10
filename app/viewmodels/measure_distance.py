from typing import Any, Optional
from app.framework.pubsub import Publisher, Subscriber
from app.services.timer import TimerService
from lib.fermento_embedded_schemas import JarSchema
from app.sensors.distance import DistanceSensor
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from app.framework.observer import Observer
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureDistanceViewmodel(BaseViewmodel, Subscriber):
    def __init__(self):
        super().__init__()
        Publisher.subscribe(self, topic=DistanceSensor.TOPIC_DISTANCE)
        Publisher.subscribe(self, topic=AppStateService.TOPIC_SELECTED_JAR_NAME)

        self._name: str = ""
        self._distance: int = 0
        self._distance_sensor: DistanceSensor = ContainerService.get_instance(DistanceSensor)
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)
        self._timer_service: TimerService = ContainerService.get_instance(TimerService)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self._notify_value_changed(name=value)

    @property
    def distance(self) -> int:
        return self._distance

    @distance.setter
    def distance(self, value: int) -> None:
        self._distance = value
        self._notify_value_changed(distance=value)

    def save_measurement(self) -> None:
        logger.info(f"Saving jar: name={self._name}, distance={self._distance}")
        message = JarSchema(name=self._name, height=self._distance).to_dict()
        self._mqtt_service.publish(topic=f"jars/create", message=message, qos=0)

    def on_view_value_changed(self, **kwargs) -> None:
        logger.debug(f"View value changed: {kwargs}")

        state = kwargs.get("state", None)
        if state == "active":
            self._distance_sensor.start()
            self._timer_service.start_timer("measure_distance", 1, True)
            Publisher.subscribe(self, topic=f"{TimerService.TOPIC_TICK}/measure_distance")

        elif state == "inactive":
            self._timer_service.stop_timer("measure_distance")
            self._distance_sensor.stop()

        save = kwargs.get("save", None)
        if save:
            self._distance_sensor.stop()
            self.save_measurement()

    def on_publisher_message_received(self, message: Any, topic: str):
        if topic == DistanceSensor.TOPIC_DISTANCE:
            self.distance = message

        elif topic == AppStateService.TOPIC_SELECTED_JAR_NAME:
            self.name = message

        elif topic == f"{TimerService.TOPIC_TICK}/measure_distance":
            self._distance_sensor.read()
