from datetime import datetime
from .base import BaseSchema


class FeedingEventSchema(BaseSchema):
    """
    Schema for telemetry data validation.
    """

    id: int
    starter: dict
    jar: dict
    timestamp: datetime

    @classmethod
    def _get_fields(cls) -> list[str]:
        return ["id", "starter", "jar", "timestamp"]
