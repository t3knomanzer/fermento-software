import asyncio
import sys
from typing import Any, Callable, Optional
from app.sensors.base import BaseSensor
from app.services import log
from app.utils.decorators import singleton
import config
from drivers.vl53l4cd import VL53L4CD
from machine import Pin, I2C
from app.framework.pubsub import Publisher


logger = log.LogServiceManager.get_logger(name=__name__)


class DistanceSensor(BaseSensor):
    TOPIC_ROOT = "distance_sensor"
    TOPIC_DISTANCE = f"{TOPIC_ROOT}/distance"

    TIMING_HIGH_SPEED = 16
    TIMING_BALANCED = 33
    TIMING_HIGH_QUALITY = 200

    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing distance sensor...")
        self._sensor: Optional[VL53L4CD] = None
        self._timing_budget: int = config.SENSOR_DISTANCE_TIMING_BUDGET
        self._distance: int = 0
        self._capture_task: Optional[asyncio.Task] = None
        self._i2c: Optional[I2C] = None

        self._setup_i2c()
        self._setup_sensor()

    @property
    def timing_budget(self) -> int:
        return self._timing_budget

    @timing_budget.setter
    def timing_budget(self, value: int):
        if self._sensor:
            self._sensor.stop_ranging()
            self._sensor.timing_budget = value
            self._sensor.start_ranging()

    @property
    def distance(self) -> int:
        return self._distance

    @distance.setter
    def distance(self, value: int):
        if self._distance != value:
            self._distance = value
            Publisher.publish(value, topic=DistanceSensor.TOPIC_DISTANCE)

    def _setup_i2c(self) -> None:
        self._i2c = I2C(0, sda=Pin(45), scl=Pin(47))

    def _setup_sensor(self, retries: int = 3) -> None:
        logger.info("Creating distance sensor...")
        while not self._sensor and retries > 0:
            try:
                self._sensor = VL53L4CD(self._i2c)
                self.timing_budget = self._timing_budget
            except Exception as e:
                logger.error(f"({retries}) Error creating distance sensor. {e}")
                retries -= 1

        if self._sensor is None:
            # Raise exception
            logger.critical("Couldn't create distance sensor.")

    def start(self) -> None:
        super().start()
        logger.info("Starting distance sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        self._sensor.start_ranging()

    def read(self) -> None:
        super().read()
        logger.info("Reading distance sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if self._capture_task and not self._capture_task.done():
            logger.warning("Ranging task already running")
            return

        self._capture_task = asyncio.create_task(self.capture_async())

    def stop(self) -> None:
        super().stop()
        logger.info("Stopping distance sensor...")
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        if not self._capture_task or self._capture_task.done() or self._capture_task.cancelled():
            logger.error("Sensor not running")
            return

        self._sensor.stop_ranging()

    async def capture_async(self) -> None:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return

        self.distance = await self._sample_average_async()
        logger.debug(f"Reading distance sensor data: {self.distance} mm")

    async def _sample_average_async(self, num_samples: int = 3) -> int:
        if not self._sensor:
            logger.error("Sensor not initialized")
            return 0

        distance = 0
        for i in range(num_samples):
            while not self._sensor.data_ready and not self._sensor.range_status == 0:
                await asyncio.sleep(0.1)

            distance += self._sensor.distance
            self._sensor.clear_interrupt()

        result = distance // num_samples
        return result
