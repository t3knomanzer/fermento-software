import asyncio
from typing import Any, Callable, Optional
from app.services import log
import config
from drivers.sht4x import SHT4x, Mode
from machine import Pin, I2C
from app.framework.pubsub import Publisher


logger = log.LogServiceManager.get_logger(name=__name__)


class TRHSensor:
    TOPIC_ROOT = "trh_sensor"
    TOPIC_DATA = f"{TOPIC_ROOT}/data"

    FREQUENCY_LOW = 1
    FREQUENCY_MED = 5
    FREQUENCY_HIGH = 33
    FREQUENCY_VERY_HIGH = 100

    def __init__(self) -> None:
        logger.info("Initializing distance sensor...")
        self._sensor: Optional[SHT4x] = None
        self._i2c: Optional[I2C] = None
        self._measure_task: Optional[asyncio.Task] = None
        self._frequency: int = TRHSensor.FREQUENCY_LOW
        self._trh: dict[str, Any] = {"t": 0.0, "rh": 0.0}

        self._setup_i2c()
        self._setup_sensor()

    @property
    def trh(self) -> dict[str, Any]:
        return self._trh

    @trh.setter
    def trh(self, value: dict[str, Any]):
        if self._trh != value:
            self._trh = value
            Publisher.publish(value, topic=self.TOPIC_DATA)

    def _setup_i2c(self) -> None:
        self._i2c = I2C(0, sda=Pin(45), scl=Pin(47))

    def _setup_sensor(self, retries: int = 3) -> None:
        logger.info("Creating TRH sensor...")
        self._sensor = SHT4x(self._i2c)
        self._sensor.mode = Mode.NOHEAT_HIGHPRECISION  # type: ignore

    def start(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if self._measure_task and not self._measure_task.done():
            logger.warning("Measure task already running")
            return

        self._measure_task = asyncio.create_task(self.read_async())

    def stop(self) -> None:
        if self._measure_task:
            self._measure_task.cancel()
            self._measure_task = None

    async def read_async(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        while True:
            t, rh = self._sensor.measurements  # type: ignore
            self.trh = {"t": t, "rh": rh}
            await asyncio.sleep(1 / self._frequency)
