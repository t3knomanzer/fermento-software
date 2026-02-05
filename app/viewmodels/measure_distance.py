from typing import Any, Optional
from app.framework.pubsub import Publisher, Subscriber
from app.sensors.distance import DistanceSensor
from app.services import log
from app.services.container import ContainerService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
from app.framework.observer import Observer
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel

logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureDistanceViewmodel(BaseViewmodel, Subscriber):
    def __init__(self):
        super().__init__()
        Publisher.subscribe(self, topic=DistanceSensor.TOPIC_DISTANCE)

        self._name: Optional[str] = None
        self._distance: int = 0
        self._distance_sensor: DistanceSensor = ContainerService.get_instance(
            DistanceSensor
        )
        self._app_state_service: AppStateService = ContainerService.get_instance(
            AppStateService
        )

    def on_view_value_changed(self, **kwargs) -> None:
        state = kwargs.get("state", None)
        if state == "active":
            self._distance_sensor.start()
            self._name = self._app_state_service.selected_name
            self._notify_value_changed(name=self._name)

        elif state == "inactive":
            self._distance_sensor.stop()

        save = kwargs.get("save", None)
        if save:
            logger.info("Save requested, stopping sensor...")

    def on_message_received(self, message: Any, topic: str):
        if topic == DistanceSensor.TOPIC_DISTANCE:
            self.distance = message
            self._notify_value_changed(distance=message)
