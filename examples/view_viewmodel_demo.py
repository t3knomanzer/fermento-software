import sys
from app.views.base import BaseView
from app.services.container import ContainerService
from app.viewmodels.base import BaseViewmodel
from typing import Any

sys.path.insert(0, "src/lib/typing")


class MyView(BaseView):
    def __init__(self):
        super().__init__()

    def on_navigated_from(self):
        print("Navigated from MyView")

    def on_navigated_to(self):
        print("Navigated to MyView")

    def on_property_changed(self, property_name: str, property_value: Any):
        print(f"Property '{property_name}' changed to {property_value}")


class MyViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
        self._some_property = None

    @property
    def some_property(self):
        return self._some_property

    @some_property.setter
    def some_property(self, value):
        self._some_property = value
        self._notify_property_changed("some_property", value)


# Register the view and viewmodel
ContainerService.register(MyView, MyViewmodel)

# Create an instance of the view (which will also create and bind the viewmodel)
view = ContainerService.create_instance(MyView)

# Example of changing a property in the viewmodel
viewmodel = view.viewmodel  # Access the bound viewmodel
viewmodel.some_property = "New Value"
