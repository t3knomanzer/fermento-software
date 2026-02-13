import asyncio
from typing import Any, Callable, Optional
from app.sensors.base import BaseSensor
from app.sensors.i2c_bus import I2CBus
from app.services.log import log
from app.services.container import ContainerService
import config
from drivers.sht4x import SHT4x, Mode
from machine import Pin, I2C

logger = log.LogServiceManager.get_logger(name=__name__)


class TRHSensor(BaseSensor):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing TRH sensor...")
        self._sensor: Optional[SHT4x] = None
        self._i2c: Optional[I2C] = None
        self._capture_task: Optional[asyncio.Task] = None
        self._trh: dict[str, Any] = {"t": 0.0, "rh": 0.0}
        self._value_changed_handlers: list[Callable[[dict[str, float]], None]] = []

        self._setup_i2c()
        self._setup_sensor()

    @property
    def trh(self) -> dict[str, float]:
        return self._trh

    @trh.setter
    def trh(self, value: dict[str, float]):
        if self._trh != value:
            self._trh = value
            self._notify_value_changed()

    def add_value_changed_handler(self, handler: Callable[[dict[str, float]], None]) -> None:
        self._value_changed_handlers.append(handler)

    def _notify_value_changed(self) -> None:
        for handler in self._value_changed_handlers:
            handler(self._trh)

    def _setup_i2c(self) -> None:
        self._i2c_bus = ContainerService.get_instance(I2CBus)
        if not self._i2c_bus:
            raise Exception("I2C bus not found in container.")

    def _setup_sensor(self, retries: int = 3) -> None:
        logger.info("Creating TRH sensor...")
        try:
            self._sensor = SHT4x(self._i2c_bus.bus)
            self._sensor.mode = Mode.NOHEAT_HIGHPRECISION  # type: ignore
        except Exception as e:
            logger.error(f"Couldn't create TRH sensor: {e}")

    def start(self) -> None:
        super().start()
        logger.info("Warming up TRH sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

    def read(self) -> None:
        super().read()
        logger.info("Reading TRH sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if self._capture_task and not self._capture_task.done():
            logger.warning("Capture task already running")
            return

        self._capture_task = asyncio.create_task(self.capture_async())

    def stop(self) -> None:
        super().stop()
        logger.info("Stopping TRH sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if not self._capture_task or self._capture_task.done() or self._capture_task.cancelled():
            logger.error("Sensor not running")
            return

        self._capture_task.cancel()
        self._capture_task = None

    async def capture_async(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        t, rh = self._sensor.measurements  # type: ignore
        logger.debug(f"Read TRH sensor data: Temperature={t}C, Humidity={rh}%")
        self.trh = {"t": t, "rh": rh}
