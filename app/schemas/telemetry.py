class TelemetrySchema:
    """
    Schema for telemetry data validation.
    """

    def __init__(
        self,
        feeding_event_id: int = 0,
        temperature: float = 0.0,
        humidity: float = 0.0,
        co2: float = 0.0,
        distance: float = 0.0,
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
