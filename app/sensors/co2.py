import asyncio
from typing import Any, Callable, Optional
from app.sensors.base import BaseSensor
from app.sensors.i2c_bus import I2CBus
from app.services.log import log
from app.services.container import ContainerService
import config
from drivers.scd4x import SCD4X
from machine import Pin, I2C

logger = log.LogServiceManager.get_logger(name=__name__)


class CO2Sensor(BaseSensor):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing CO2 sensor...")
        self._sensor: Optional[SCD4X] = None
        self._i2c: Optional[I2C] = None
        self._co2: int = 0
        self._capture_task: Optional[asyncio.Task] = None
        self._value_changed_handlers: list[Callable[[int], None]] = []

        self._setup_i2c()
        self._setup_sensor()

    @property
    def co2(self) -> int:
        return self._co2

    @co2.setter
    def co2(self, value: int):
        if self._co2 != value:
            self._co2 = value
            self._notify_value_changed()

    def add_value_changed_handler(self, handler: Callable[[int], None]) -> None:
        self._value_changed_handlers.append(handler)

    def _notify_value_changed(self) -> None:
        for handler in self._value_changed_handlers:
            handler(self._co2)

    def _setup_i2c(self) -> None:
        self._i2c_bus = ContainerService.get_instance(I2CBus)
        if not self._i2c_bus:
            raise Exception("I2C bus not found in container.")

    def _setup_sensor(self, retries: int = 3) -> None:
        logger.info("Creating CO2 sensor...")
        try:
            self._sensor = SCD4X(self._i2c_bus.bus)
        except Exception as e:
            logger.error(f"Couldn't create CO2 sensor: {e}")

    def start(self) -> None:
        super().start()
        logger.info("Starting CO2 sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        self._sensor.start_periodic_measurement()

    def read(self) -> None:
        super().read()
        logger.info("Reading CO2 sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if self._capture_task and not self._capture_task.done():
            logger.warning("Capture task already running")
            return

        self._capture_task = asyncio.create_task(self.capture_async())

    def stop(self) -> None:
        super().stop()
        logger.info("Stopping CO2 sensor...")
        if not self._sensor:
            logger.warning("Sensor not initialized")
            return

        if not self._capture_task:
            logger.warning("Sensor not running")
            return

        if self._capture_task.done() or self._capture_task.cancelled():
            logger.warning("Capture task already completed")
            return

        self._sensor.stop_periodic_measurement()
        self._capture_task.cancel()
        self._capture_task = None

    async def capture_async(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        while not self._sensor.data_ready:
            await asyncio.sleep(0.1)

        self.co2 = self._sensor.CO2
        logger.debug(f"Read CO2 sensor data: {self.co2} ppm")
