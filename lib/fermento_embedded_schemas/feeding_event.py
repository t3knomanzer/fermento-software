from .base import BaseSchema
import time


class FeedingEventSchema(BaseSchema):
    """
    Schema for telemetry data validation.
    """

    id: int
    starter: dict
    jar: dict
    timestamp: str

    @classmethod
    def from_dict(cls, data: dict) -> "FeedingEventSchema":
        return super().from_dict(data)  # type: ignore

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "id",
            "starter",
            "jar",
            "timestamp",
        ]
