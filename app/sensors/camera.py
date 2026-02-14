import asyncio
from typing import Any, Callable, Optional
from app.sensors.base import BaseSensor
from app.services.log import log
from camera import Camera
import config

logger = log.LogServiceManager.get_logger(name=__name__)


class CameraSensor(BaseSensor):
    def __init__(self) -> None:
        super().__init__()
        self._sensor: Optional[Camera] = None
        self._frame: Optional[bytes] = None
        self._value_changed_handlers: list[Callable[[Optional[bytes]], None]] = []

        self._setup_sensor()

    @property
    def frame(self) -> Optional[bytes]:
        return self._frame

    def add_value_changed_handler(self, handler: Callable[[Optional[bytes]], None]) -> None:
        self._value_changed_handlers.append(handler)

    def _notify_value_changed(self) -> None:
        for handler in self._value_changed_handlers:
            handler(self._frame)

    def _setup_sensor(self, retries: int = 3) -> None:
        logger.info("Setting up camera...")
        try:
            self._sensor = Camera(
                frame_size=config.CAMERA_FRAME_SIZE,
                pixel_format=config.CAMERA_PIXEL_FORMAT,
                jpeg_quality=config.CAMERA_JPEG_QUALITY,
                fb_count=config.CAMERA_FB_COUNT,
                init=False,
            )
        except Exception as e:
            logger.error(f"Couldn't create camera {e}")

    def start(self) -> None:
        super().start()
        logger.info("Starting camera...")
        if not self._sensor:
            logger.error("Camera not initialized")
            return
        try:
            self._sensor.init()
        except Exception as e:
            logger.error(f"Couldn't initialize camera {e}")

    def read(self) -> None:
        super().read()
        logger.info("Reading camera...")
        if not self._sensor:
            logger.error("Camera not initialized")
            return

        self._frame = self._sensor.capture()
        self._notify_value_changed()

    def stop(self) -> None:
        super().stop()
        logger.info("Stopping camera...")
        if not self._sensor:
            logger.error("Camera not initialized")
            return

        self._capture_task = None
        self._sensor.deinit()
