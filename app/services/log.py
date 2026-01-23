import os

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
    _filepath = ""
    _services = {}
    _level = INFO

    @classmethod
    def set_level(cls, level: int) -> None:
        cls._level = level
        for k, v in enumerate(cls._services):
            v.set_level(level)

    @classmethod
    def set_filepath(cls, filepath: str) -> None:
        # Remove the log file if it exists
        try:
            os.remove(filepath)
        except OSError:
            print(f"Couldn't delete log file {filepath}")
        cls._filepath = filepath

    @classmethod
    def get_logger(cls, name: str | None = None) -> "LogService":
        if name not in cls._services:
            cls._services[name] = LogService(name, cls._filepath, cls._level)
        return cls._services[name]


class LogService:
    def __init__(self, name: str, filepath: str, level: int = INFO):
        self._name = name
        self._filepath = filepath
        self._level = level

    def set_level(self, level: str) -> None:
        self._level = level

    def log(self, message: str, level: int, name: str | None = None):
        if level >= self._level:
            print(f"[{LEVEL_NAMES[level]}][{name or self._name}] {message}")

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
