import asyncio
from typing import cast
from app.services import log
from app.services.app import ApplicationService
from app.services.mqtt import MqttService
from app.services.navigation import NavigationService
from app.services.network import NetworkService
from app.viewmodels.base import BaseViewmodel
from app.viewmodels.menu import MenuViewmodel
from app.viewmodels.splash import SplashViewmodel
from app.views.menu import MenuView
from app.views.splash import SplashView

logger = log.LogServiceManager.get_logger(name=__name__)


class ApplicationViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()

        ApplicationService.create_view(SplashView, SplashViewmodel)
        ApplicationService.create_view(MenuView, MenuViewmodel)

    def start(self):
        logger.info("Creating view...")
        asyncio.create_task(self.xx())
        NavigationService.navigate_to(SplashView)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    async def xx(self):
        await asyncio.sleep(1)
        view = ApplicationService.get_view(SplashView)
        if view:
            a = cast(SplashViewmodel, view.viewmodel)
            a.splash_message = "Hello sir!"
