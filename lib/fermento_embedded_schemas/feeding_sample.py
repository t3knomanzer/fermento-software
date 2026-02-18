from .base import BaseSchema


class FeedingSampleSchema(BaseSchema):
    """
    Schema for telemetry data validation.
    """

    bundle_id: int
    feeding_event_id: int
    temperature: float
    humidity: float
    co2: float
    distance: float

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "bundle_id",
            "feeding_event_id",
            "temperature",
            "humidity",
            "co2",
            "distance",
        ]
