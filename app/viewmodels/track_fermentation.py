from typing import Any, Optional, cast
from app.framework.pubsub import Publisher, Subscriber
from app.schemas.feeding_event import FeedingEventSchema
from app.schemas.feeding_sample import FeedingSampleSchema
from app.schemas.jar import JarSchema
from app.sensors.co2 import CO2Sensor
from app.sensors.distance import DistanceSensor
from app.sensors.trh import TRHSensor
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.services.timer import TimerService
from app.viewmodels.base import BaseViewmodel
from app.framework.observer import Observer
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel
import json

logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFermentationViewmodel(BaseViewmodel, Subscriber):
    def __init__(self):
        super().__init__()
        Publisher.subscribe(self, topic=DistanceSensor.TOPIC_DISTANCE)
        Publisher.subscribe(self, topic=TRHSensor.TOPIC_TRH)
        Publisher.subscribe(self, topic=CO2Sensor.TOPIC_CO2)
        Publisher.subscribe(self, topic=AppStateService.TOPIC_SELECTED_FEEDING_EVENT)

        self._distance: int = 0
        self._trh: dict[str, Any] = {"t": 0.0, "rh": 0.0}
        self._co2: int = 0
        self._feeding_event: Optional[FeedingEventSchema] = None
        self._jar_name: str = ""
        self._starter_name: str = ""

        self._distance_sensor: DistanceSensor = ContainerService.get_instance(DistanceSensor)
        self._trh_sensor: TRHSensor = ContainerService.get_instance(TRHSensor)
        self._co2_sensor: CO2Sensor = ContainerService.get_instance(CO2Sensor)
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)
        self._timer_service: TimerService = ContainerService.get_instance(TimerService)

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def trh(self) -> dict[str, Any]:
        return self._trh

    @property
    def co2(self) -> int:
        return self._co2

    @property
    def jar_name(self) -> str:
        return self._jar_name

    @property
    def starter_name(self) -> str:
        return self._starter_name

    @distance.setter
    def distance(self, value: int) -> None:
        if self._distance != value:
            self._distance = value
            self._notify_value_changed(distance=value)

    @trh.setter
    def trh(self, value: dict[str, Any]) -> None:
        if self._trh != value:
            self._trh = value
            self._notify_value_changed(trh=value)

    @co2.setter
    def co2(self, value: int) -> None:
        if self._co2 != value:
            self._co2 = value
            self._notify_value_changed(co2=value)

    @jar_name.setter
    def jar_name(self, value: str) -> None:
        if self._jar_name != value:
            self._jar_name = value
            self._notify_value_changed(jar_name=value)

    @starter_name.setter
    def starter_name(self, value: str) -> None:
        if self._starter_name != value:
            self._starter_name = value
            self._notify_value_changed(starter_name=value)

    def on_view_value_changed(self, **kwargs) -> None:
        state = kwargs.get("state", None)
        if state == "active":
            self._distance_sensor.start()
            self._trh_sensor.start()
            self._co2_sensor.start()
            self._timer_service.start_timer("preview", 1, True)
            Publisher.subscribe(self, topic=f"{TimerService.TOPIC_TICK}/preview")

        elif state == "active_capture":
            self._timer_service.stop_timer("preview")
            self._timer_service.start_timer("capture", 5, True)
            Publisher.subscribe(self, topic=f"{TimerService.TOPIC_TICK}/capture")

        elif state == "inactive":
            self._timer_service.stop_timer("capture")
            self._distance_sensor.stop()
            self._trh_sensor.stop()
            self._co2_sensor.stop()

    def on_publisher_message_received(self, message: Any, topic: str):
        if topic == DistanceSensor.TOPIC_DISTANCE:
            self.distance = message

        elif topic == TRHSensor.TOPIC_TRH:
            self.trh = message

        elif topic == CO2Sensor.TOPIC_CO2:
            self.co2 = message

        elif topic == AppStateService.TOPIC_SELECTED_FEEDING_EVENT:
            self._feeding_event = message
            if self._feeding_event is not None:
                self.jar_name = self._feeding_event.jar["name"]
                self.starter_name = self._feeding_event.starter["name"]

        elif topic == f"{TimerService.TOPIC_TICK}/preview":
            self._distance_sensor.read()
            self._trh_sensor.read()
            self._co2_sensor.read()

        elif topic == f"{TimerService.TOPIC_TICK}/capture":
            self._distance_sensor.read()
            self._trh_sensor.read()
            self._co2_sensor.read()
            # Submit data to MQTT
            logger.info(
                f"Saving sample: Distance: {self._distance}, TRH: {self._trh}, CO2: {self._co2}"
            )
            message = FeedingSampleSchema(
                feeding_event_id=0,
                temperature=self._trh.get("t", 0.0),
                humidity=self._trh.get("rh", 0.0),
                co2=self._co2,
                distance=self._distance,
            ).to_dict()
            self._mqtt_service.publish(topic=f"feeding_samples/create", message=message, qos=0)
