class BaseSensor:
    FREQUENCY_VERY_LOW = 1 / 60  # 1 measurement per minute
    FREQUENCY_LOW = 1 / 30  # 1 measurements every 30 seconds
    FREQUENCY_MED = 1 / 15  # 1 measurements every 15 seconds
    FREQUENCY_HIGH = 1 / 5  # 1 measurements every 5 seconds
    FREQUENCY_VERY_HIGH = 1  # 1 measurement per second

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
