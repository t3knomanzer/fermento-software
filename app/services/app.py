from typing import Optional
from app.viewmodels.base import BaseViewmodel
from app.views.base import BaseView


class ApplicationService:
    _view_type_instance_map = {}

    @classmethod
    def create_view(
        cls, view_class: type, viewmodel_class: type, reuse_instance: bool = True
    ) -> BaseView:
        if view_class in cls._view_type_instance_map and reuse_instance:
            return cls._view_type_instance_map[view_class]

        viewmodel: BaseViewmodel = viewmodel_class()
        view: BaseView = view_class()
        viewmodel.bind_view(view)
        view.bind_viewmodel(viewmodel)

        cls._view_type_instance_map[view_class] = view

        return view

    @classmethod
    def get_view(cls, instance_type: type) -> Optional[BaseView]:
        return cls._view_type_instance_map.get(instance_type, None)
