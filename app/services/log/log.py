from typing import Optional

DEBUG = 0
INFO = 10
WARNING = 20
ERROR = 30
CRITICAL = 40

LEVEL_NAMES = {
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARNING: "WARNING",
    ERROR: "ERROR",
    CRITICAL: "CRITICAL",
}


class LogServiceManager:
    _services = {}
    _level = INFO
    _handlers = []

    @classmethod
    def set_level(cls, level: int) -> None:
        cls._level = level

    @classmethod
    def initialize(cls, level: int = INFO) -> None:
        cls.set_level(level)

    @classmethod
    def get_logger(cls, name: str | None = None) -> "LogService":
        if name not in cls._services:
            logger = LogService(name, cls._level)
            cls._services[name] = logger
            for handler in cls._handlers:
                logger.register_handler(handler)

        return cls._services[name]

    @classmethod
    def register_handler(cls, handler: BaseHandler):
        cls._handlers.append(handler)

        for logger in cls._services.values():
            logger.register_handler(handler)


class LogService:
    def __init__(self, name: str, level: int = INFO):
        self._name = name
        self._level = level
        self._handlers = []

    def register_handler(self, handler):
        self._handlers.append(handler)

    def set_level(self, level: int) -> None:
        self._level = level

    def log(self, message: str, level: int, name: Optional[str] = None):
        if level >= self._level:
            for handler in self._handlers:
                try:
                    handler.log(message, LEVEL_NAMES[level], name or self._name)
                except:
                    print(f"Failed to log message with handler {handler}: {message}")

    def info(self, message: str):
        self.log(message, INFO)

    def warning(self, message: str):
        self.log(message, WARNING)

    def error(self, message: str):
        self.log(message, ERROR)

    def critical(self, message: str):
        self.log(message, CRITICAL)

    def debug(self, message: str):
        self.log(message, DEBUG)
