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
    def from_dict(cls, data: dict) -> "FeedingEventSchema":
        if "timestamp" in data and isinstance(data["timestamp"], str):
            timestamp = data["timestamp"].replace("Z", "+00:00")
            data["timestamp"] = datetime.fromisoformat(timestamp)
        return super().from_dict(data)  # type: ignore

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "id",
            "starter",
            "jar",
            "timestamp",
        ]
