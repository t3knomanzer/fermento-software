from typing import Any, Optional
from lib.fermento_embedded_schemas.feeding_event import FeedingEventSchema
from lib.fermento_embedded_schemas.feeding_sample import FeedingSampleSchema
from app.sensors.co2 import CO2Sensor
from app.sensors.distance import DistanceSensor
from app.sensors.trh import TRHSensor
from app.services.log import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.services.timer import TimerService
from app.viewmodels.base import BaseViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class TrackFermentationViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
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

        self._distance_sensor.add_value_changed_handler(self._on_distance_changed)
        self._trh_sensor.add_value_changed_handler(self._on_trh_changed)
        self._co2_sensor.add_value_changed_handler(self._on_co2_changed)
        self._app_state_service.add_selected_feeding_event_handler(
            self._on_selected_feeding_event_changed
        )
        self._timer_service.add_tick_handler(self._on_timer_tick)

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
        logger.debug(f"View value changed: {kwargs}")

        state = kwargs.get("state", None)
        if state == "active":
            self._distance_sensor.start()
            self._trh_sensor.start()
            self._co2_sensor.start()
            self._timer_service.start_timer("preview", 1, True)

        elif state == "active_capture":
            self._timer_service.stop_timer("preview")
            self._timer_service.start_timer("capture", 60, True)

        elif state == "inactive":
            self._timer_service.stop_timer("capture")
            self._distance_sensor.stop()
            self._trh_sensor.stop()
            self._co2_sensor.stop()

    def _on_distance_changed(self, distance: int) -> None:
        self.distance = distance

    def _on_trh_changed(self, trh: dict[str, Any]) -> None:
        self.trh = trh

    def _on_co2_changed(self, co2: int) -> None:
        self.co2 = co2

    def _on_selected_feeding_event_changed(
        self, feeding_event: Optional[FeedingEventSchema]
    ) -> None:
        self._feeding_event = feeding_event
        if self._feeding_event is not None:
            self.jar_name = self._feeding_event.jar["name"]
            self.starter_name = self._feeding_event.starter["name"]

    def _on_timer_tick(self, timer_name: str) -> None:
        if timer_name == "preview":
            logger.debug("Preview timer tick - reading sensors")
            self._distance_sensor.read()
            self._trh_sensor.read()
            self._co2_sensor.read()

        elif timer_name == "capture":
            self._distance_sensor.read()
            self._trh_sensor.read()
            self._co2_sensor.read()
            # Submit data to MQTT
            logger.info(
                f"Saving sample: Distance: {self._distance}, TRH: {self._trh}, CO2: {self._co2}"
            )
            message = FeedingSampleSchema(
                feeding_event_id=self._feeding_event.id if self._feeding_event else None,
                temperature=self._trh.get("t", 0.0),
                humidity=self._trh.get("rh", 0.0),
                co2=self._co2,
                distance=self._distance,
            ).to_dict()
            self._mqtt_service.publish(topic=f"feeding_samples/create", message=message, qos=0)
