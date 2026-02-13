from app.services.log.handlers.base import BaseHandler
from app.utils.time import now_isoformat, ntp_is_set


class ConsoleHandler(BaseHandler):
    def __init__(self):
        pass

    def _build_message(self, message: str, level: str, name: str | None = None) -> str:
        time = f"[{now_isoformat()}]" if ntp_is_set() else "[0000-00-00T00:00:00Z]"
        return f"{time}[{level}][{name}] {message}"

    def log(self, message: str, level: str, name: str | None = None):
        msg = self._build_message(message, level, name)
        print(msg)
