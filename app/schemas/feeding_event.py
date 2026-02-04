class FeedingEventSchema:
    """
    Schema for feeding event data validation.
    """

    def __init__(
        self,
        id: int,
        date: str,
        starter_id: int,
        starter_ratio: float,
        water_ratio: float,
        flour_ratio: float,
        flour_blend_id: int,
        jar_id: int,
    ) -> None:
        self.id: int = id
        self.date: str = date
        self.starter_id: int = starter_id
        self.starter_ratio: float = starter_ratio
        self.water_ratio: float = water_ratio
        self.flour_ratio: float = flour_ratio
        self.flour_blend_id: int = flour_blend_id
        self.jar_id: int = jar_id

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "starter_id": self.starter_id,
            "starter_ratio": self.starter_ratio,
            "water_ratio": self.water_ratio,
            "flour_ratio": self.flour_ratio,
            "flour_blend_id": self.flour_blend_id,
            "jar_id": self.jar_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        date_time = data["date"].split("T")
        time_zone = date_time[1].split(".")
        date = f"{date_time[0]} {time_zone[0]}"

        return FeedingEventSchema(
            id=data["id"],
            date=date,
            starter_id=data["starter_id"],
            starter_ratio=data["starter_ratio"],
            water_ratio=data["water_ratio"],
            flour_ratio=data["flour_ratio"],
            flour_blend_id=data["flour_blend_id"],
            jar_id=data["jar_id"],
        )
