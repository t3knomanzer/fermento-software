from typing import Optional
from app.services import log
from app.services.container import ContainerService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
import config
import random
from app.resources.names import NAMES


logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureNameSelectViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
        self._choices: set[str] = set()
        self._choice: Optional[str] = None
        self._app_state_service: AppStateService = ContainerService.get_instance(AppStateService)

    @property
    def choices(self):
        return self._choices

    def _generate_name_choices(self, num_choices=config.MEASURE_MAX_CHOICES):
        logger.debug("Generating name choices...")
        while len(self._choices) < num_choices:
            index = random.randint(0, len(NAMES) - 1)
            name = NAMES[index]
            self._choices.add(name)
        self._notify_value_changed(choices=self.choices)

    def on_view_value_changed(self, **kwargs) -> None:
        logger.debug(f"View value changed: {kwargs}")

        state = kwargs.get("state", None)
        if state == "active":
            self._generate_name_choices()

        choice = kwargs.get("choice", None)
        if choice:
            self._app_state_service.selected_jar_name = choice
            self._choice = choice
