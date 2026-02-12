from time import struct_time
from .base import BaseSchema
from app.utils.time import time as t
import time

class FeedingEventSchema(BaseSchema):
    """
    Schema for telemetry data validation.
    """

    id: int
    starter: dict
    jar: dict
    timestamp: struct_time

    @classmethod
    def from_dict(cls, data: dict) -> "FeedingEventSchema":
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = time.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S%")
        return super().from_dict(data)  # type: ignore

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "id",
            "starter",
            "jar",
            "timestamp",
        ]
