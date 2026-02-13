from typing import Optional
from app.services.log.log import LogServiceManager
from machine import Pin, I2C

logger = LogServiceManager.get_logger(name=__name__)


class I2CBus:
    def __init__(self):
        self._id: Optional[int] = None
        self._sda_pin: Optional[int] = None
        self._scl_pin: Optional[int] = None
        self._bus: Optional[I2C] = None

    @property
    def bus(self):
        return self._bus

    def start(self, id: int = 0, sda_pin: int = 21, scl_pin: int = 22) -> None:
        logger.debug(f"Initializing I2C bus {id} with SDA pin {sda_pin} and SCL pin {scl_pin}...")
        self._id = id
        self._sda_pin = sda_pin
        self._scl_pin = scl_pin

        try:
            self._bus = I2C(self._id, sda=Pin(self._sda_pin), scl=Pin(self._scl_pin))
            logger.info(f"I2C bus {self._id} initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing I2C bus {self._id}: {e}")
            raise
