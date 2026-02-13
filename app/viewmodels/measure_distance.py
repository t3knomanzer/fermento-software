from app.services.timer import TimerService
from lib.fermento_embedded_schemas import JarSchema
from app.sensors.distance import DistanceSensor
from app.services.log import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureDistanceViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
        self._name: str = ""
        self._distance: int = 0
        self._distance_sensor: DistanceSensor = ContainerService.get_instance(DistanceSensor)
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)
        self._mqtt_service: MqttService = ContainerService.get_instance(MqttService)
        self._timer_service: TimerService = ContainerService.get_instance(TimerService)

        self._distance_sensor.add_value_changed_handler(self._on_distance_changed)
        self._app_state_service.add_selected_jar_name_handler(self._on_selected_jar_name_changed)
        self._timer_service.add_tick_handler(self._on_timer_tick)

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

        elif state == "inactive":
            self._timer_service.stop_timer("measure_distance")
            self._distance_sensor.stop()

        save = kwargs.get("save", None)
        if save:
            self._distance_sensor.stop()
            self.save_measurement()

    def _on_distance_changed(self, distance: int) -> None:
        self.distance = distance

    def _on_selected_jar_name_changed(self, name: str) -> None:
        self.name = name

    def _on_timer_tick(self, timer_name: str) -> None:
        if timer_name == "measure_distance":
            logger.debug("Measure distance timer tick - reading distance")
            self._distance_sensor.read()
