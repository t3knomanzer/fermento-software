import asyncio
from typing import cast
from app.services import log
from app.services.app import ApplicationService
from app.services.mqtt import MqttService
from app.services.navigation import NavigationService
from app.services.network import NetworkService
from app.utils.time import set_ntp_time
from app.viewmodels.base import BaseViewmodel
from app.viewmodels.menu import MenuViewmodel
from app.viewmodels.settings import SettingsViewmodel
from app.viewmodels.splash import SplashViewmodel
from app.views.menu import MenuView
from app.views.settings import SettingsView
from app.views.splash import SplashView
from lib.pubsub.pubsub import Publisher

logger = log.LogServiceManager.get_logger(name=__name__)


class ApplicationViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()

        ApplicationService.create_view(SplashView, SplashViewmodel)
        ApplicationService.create_view(MenuView, MenuViewmodel)
        ApplicationService.create_view(SettingsView, SettingsViewmodel)

    async def _update_splash(self, message):
        Publisher.publish(message, "splash_message")
        await asyncio.sleep(0.1)

    def start(self):
        logger.info("Starting...")
        asyncio.create_task(self.init_services())
        NavigationService.navigate_to(SplashView)

    async def init_services(self):
        await asyncio.sleep(0.1)

        await self._update_splash("Connecting WiFi...")
        self._net_service = NetworkService()
        connected = None
        try:
            connected = self._net_service.connect()
        except Exception as e:
            logger.critical(f"Error connecting to WiFi. {e}")
            await self._update_splash("WiFi error!")
            return

        if not connected:
            await self._update_splash("Configure WiFi")
            logger.info("Starting web server...")
            try:
                self._net_service.start_server()
            except Exception as e:
                logger.critical(f"Error starting web server. {e}")
                await self._update_splash("Web Server error!")
                return

        logger.info("Syncing time...")
        await self._update_splash("Syncing time...")
        set_ntp_time()

        await self._update_splash("Setting up services...")
        logger.info("Initializing MQTT...")
        try:
            self._mqtt_service = MqttService()
            self._mqtt_service.connect()
            self._mqtt_service.subscribe_topic("fermento/#")
        except OSError:
            logger.critical(f"Error connecting to MQTT broker.")
            await self._update_splash("Service error!")
            return

        await self._update_splash("Welcome!")
        await asyncio.sleep(0.5)
        NavigationService.navigate_to(MenuView)
