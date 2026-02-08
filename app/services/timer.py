import asyncio

from app.framework.pubsub import Publisher


class TimerService:
    TOPIC_ROOT = "timer"
    TOPIC_TICK = f"{TOPIC_ROOT}/tick"

    def __init__(self):
        self._timer_tasks: dict[str, asyncio.Task] = {}

    def start_timer(self, name: str, duration: int, loop: bool = False) -> None:
        if name in self._timer_tasks and not self._timer_tasks[name].done():
            self._timer_tasks[name].cancel()
        self._timer_tasks[name] = asyncio.create_task(self._run_timer(name, duration, loop))

    async def _run_timer(self, name: str, duration: int, loop: bool = False) -> None:
        if loop:
            while True:
                await asyncio.sleep(duration)
                Publisher.publish({"timer": "tick"}, topic=f"{self.TOPIC_TICK}/{name}")
        else:
            await asyncio.sleep(duration)
            Publisher.publish({"timer": "tick"}, topic=f"{self.TOPIC_TICK}/{name}")

    def stop_timer(self, name: str) -> None:
        if name in self._timer_tasks and not self._timer_tasks[name].done():
            self._timer_tasks[name].cancel()
