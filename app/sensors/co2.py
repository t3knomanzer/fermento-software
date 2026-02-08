import asyncio
from typing import Any, Callable, Optional
from app.sensors.base import BaseSensor
from app.services import log
import config
from drivers.scd4x import SCD4X
from machine import Pin, I2C
from app.framework.pubsub import Publisher


logger = log.LogServiceManager.get_logger(name=__name__)


class CO2Sensor(BaseSensor):
    TOPIC_ROOT = "co2_sensor"
    TOPIC_CO2 = f"{TOPIC_ROOT}/co2"

    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing CO2 sensor...")
        self._sensor: Optional[SCD4X] = None
        self._i2c: Optional[I2C] = None
        self._co2: int = 0
        self._frequency: float = BaseSensor.FREQUENCY_HIGH
        self._read_task: Optional[asyncio.Task] = None

        self._setup_i2c()
        self._setup_sensor()

    @property
    def co2(self) -> int:
        return self._co2

    @co2.setter
    def co2(self, value: int):
        if self._co2 != value:
            self._co2 = value
            Publisher.publish(value, topic=self.TOPIC_CO2)

    def _setup_i2c(self) -> None:
        self._i2c = I2C(0, sda=Pin(45), scl=Pin(47))

    def _setup_sensor(self, retries: int = 3) -> None:
        logger.info("Creating CO2 sensor...")
        self._sensor = SCD4X(self._i2c)

    def start(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if self._read_task and not self._read_task.done():
            logger.warning("Read task already running")
            return

        self._sensor.start_periodic_measurement()
        self._read_task = asyncio.create_task(self.read_async())

    def stop(self) -> None:
        if self._read_task:
            if self._sensor:
                self._sensor.stop_periodic_measurement()

            self._read_task.cancel()
            self._read_task = None

    async def read_async(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        logger.info("Starting CO2 read loop...")
        while True:
            if self._sensor.data_ready:
                self.co2 = self._sensor.CO2
                logger.debug(f"Reading CO2 sensor data: {self.co2} ppm")
                await asyncio.sleep(1 / self._frequency)
            else:
                await asyncio.sleep(0.1)
