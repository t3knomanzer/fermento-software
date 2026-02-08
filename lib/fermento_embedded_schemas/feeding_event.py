from lib.fermento_embedded_schemas.base import BaseSchema


class FeedingEventSchema(BaseSchema):
    """
    Schema for telemetry data validation.
    """

    id: int
    date: str
    starter: dict
    jar: dict

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "id",
            "date",
            "starter",
            "jar",
        ]
