from app.services.log.handlers.base import BaseHandler


class FileHandler(BaseHandler):
    def __init__(self):
        pass

    def log(self, message: str, level: str, name: str | None = None):
        pass
