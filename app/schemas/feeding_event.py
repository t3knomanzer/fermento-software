from app.schemas.base import BaseSchema


class FeedingEventSchema(BaseSchema):
    """
    Schema for telemetry data validation.
    """

    schema: tuple[int, int, int]
    device_id: str
    message_id: str
    timestamp: str
    date: str
    starter_id: int
    starter: dict
    starter_ratio: float
    water_ratio: float
    flour_ratio: float
    flour_blend_id: int
    flour: dict
    jar_id: int
    jar: dict

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "schema",
            "device_id",
            "message_id",
            "timestamp",
            "date",
            "starter_id",
            "starter",
            "starter_ratio",
            "water_ratio",
            "flour_ratio",
            "flour_blend_id",
            "flour",
            "jar_id",
            "jar",
        ]
