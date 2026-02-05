from typing import Any, Optional
from app.framework.observer import Observable, Observer
from app.services import log
from app.viewmodels.base import BaseViewmodel
from app.views.base import BaseView

logger = log.LogServiceManager.get_logger(name=__name__)


class RegisteredType:
    def __init__(self, type_: type, strategy: int) -> None:
        self.type = type_
        self.strategy = strategy
        self.instances: list[object] = list()


class ContainerService:
    STRATEGY_INSTANCED = 0
    STRATEGY_SINGLETON = 1

    _type_map: dict[type, RegisteredType] = {}

    @classmethod
    def register_type(cls, type_: type, strategy: int = STRATEGY_SINGLETON) -> None:
        if type_ in cls._type_map:
            return
        cls._type_map[type_] = RegisteredType(type_, strategy)

    @classmethod
    def get_instance(cls, type_: type) -> Any:
        if not type_ in cls._type_map:
            raise ValueError(f"Type {type_.__name__} is not registered.")

        registered_type = cls._type_map[type_]
        if registered_type.strategy == ContainerService.STRATEGY_INSTANCED or (
            registered_type.strategy == ContainerService.STRATEGY_SINGLETON
            and len(registered_type.instances) == 0
        ):
            instance = registered_type.type()
            registered_type.instances.append(instance)
            return instance
        else:
            return registered_type.instances[0]
