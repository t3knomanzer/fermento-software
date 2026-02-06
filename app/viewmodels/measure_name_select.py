from typing import Any, Optional
from app.framework.pubsub import Publisher
from app.services import log
from app.services.container import ContainerService
from app.services.state import AppStateService
from app.viewmodels.base import BaseViewmodel
import config
import random
from app.resources.names import NAMES


logger = log.LogServiceManager.get_logger(name=__name__)


class MeasureNameSelectViewmodel(BaseViewmodel):
    TOPIC_ROOT = "measure_name_select"
    TOPIC_CHOICE_SELECTED = f"{TOPIC_ROOT}/choice_selected"

    def __init__(self):
        super().__init__()
        self._choices: set[str] = set()
        self._choice: Optional[str] = None
        self._app_state_service: AppStateService = ContainerService.get_instance(
            AppStateService
        )

    @property
    def choices(self):
        return self._choices

    def _generate_name_choices(self, num_choices=config.MEASURE_NAME_MAX_CHOICES):
        logger.info("Generating name choices...")
        while len(self._choices) < num_choices:
            index = random.randint(0, len(NAMES) - 1)
            name = NAMES[index]
            self._choices.add(name)
        self._notify_value_changed(choices=self.choices)

    def on_view_value_changed(self, **kwargs) -> None:
        state = kwargs.get("state", None)
        if state == "active":
            logger.info("Received status active, generating choices...")
            self._generate_name_choices()

        choice = kwargs.get("choice", None)
        if choice:
            logger.info(f"Received picked choice: {choice}")
            self._app_state_service.selected_jar_name = choice
            self._choice = choice
