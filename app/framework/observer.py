from app.services import log


class Observer:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def on_observable_changed(self, **kwargs) -> None:
        raise NotImplementedError("Subclasses must implement on_observable_changed.")


class Observable:
    def __init__(self) -> None:
        self._observers: set[Observer] = set()

    def register_observer(self, observer: Observer) -> None:
        self._observers.add(observer)

    def _notify_observers(self, **kwargs) -> None:
        for observer in self._observers:
            observer.on_observable_changed(**kwargs)
