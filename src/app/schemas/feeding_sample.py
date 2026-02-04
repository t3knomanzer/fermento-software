class FeedingSampleSchema:
    """
    Schema for feeding sample data validation.
    """

    def __init__(
        self,
        feeding_event_id: int,
        temperature: float,
        humidity: float,
        co2: float,
        distance: float,
    ) -> None:
        self.feeding_event_id: int = feeding_event_id
        self.temperature: float = temperature
        self.humidity: float = humidity
        self.co2: float = co2
        self.distance: float = distance

    def to_dict(self):
        return {
            "feeding_event_id": self.feeding_event_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "co2": self.co2,
            "distance": self.distance,
        }
