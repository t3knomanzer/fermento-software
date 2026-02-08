from lib.fermento_embedded_schemas.base import BaseSchema


class JarSchema(BaseSchema):
    """
    Schema for jar data validation.
    """

    name: str
    height: float

    @classmethod
    def _get_fields(cls) -> list[str]:
        return [
            "name",
            "height",
        ]
