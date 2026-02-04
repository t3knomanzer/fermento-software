class Publisher:
    _subscribers: dict[str, list["Subscriber"]] = {}

    @classmethod
    def subscribe(cls, subscriber: "Subscriber", topic: str) -> None:
        if topic not in cls._subscribers:
            cls._subscribers[topic] = []

        if subscriber not in cls._subscribers[topic]:
            cls._subscribers[topic].append(subscriber)

    @classmethod
    def publish(cls, message: str, topic: str):
        if topic not in cls._subscribers:
            print(f"There are no subscribers to topic {topic}")
            return

        for subscriber in cls._subscribers[topic]:
            subscriber.receive(message)


class Subscriber:
    def receive(self, message):
        raise NotImplementedError("Subclasses need to implement the receive method.")
