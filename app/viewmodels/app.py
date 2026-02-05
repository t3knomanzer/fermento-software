import asyncio
from typing import Optional, cast
from app.sensors.distance import DistanceSensor
from app.services import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.navigation import NavigationService
from app.services.network import NetworkService
from app.utils.time import set_ntp_time
from app.viewmodels.base import BaseViewmodel
from app.viewmodels.measure_distance import MeasureDistanceViewmodel
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel
from app.viewmodels.settings import SettingsViewmodel
from app.viewmodels.splash import SplashViewmodel
from app.views.base import BaseView
from app.views.measure_distance import MeasureDistanceView
from app.views.measure_name_select import MeasureNameSelectView
from app.views.menu import MenuView
from app.views.settings import SettingsView
from app.views.splash import SplashView

logger = log.LogServiceManager.get_logger(name=__name__)


class ApplicationViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
        self._net_service: Optional[NetworkService] = None
        self._mqtt_service: Optional[MqttService] = None
        self._distance_sensor: Optional[DistanceSensor] = None

    def start(self) -> None:
        logger.info("Starting...")
        self._register_types()
        self._bind_views_viewmodels()
        asyncio.create_task(self._init_services_async())
        NavigationService.navigate_to(SplashView)

    async def _set_splash_message_async(self, message: str) -> None:
        splash_vm = ContainerService.get_instance(SplashViewmodel)
        splash_vm = cast(SplashViewmodel, splash_vm)
        splash_vm.message = message
        # Yield to allow UI update on event loop
        await asyncio.sleep(0.1)

    def _register_types(self) -> None:
        logger.info("Registering types...")
        # Views
        ContainerService.register_type(SplashView)
        ContainerService.register_type(MenuView)
        ContainerService.register_type(SettingsView)
        ContainerService.register_type(MeasureNameSelectView)
        ContainerService.register_type(MeasureDistanceView)
        ContainerService.register_type(SettingsView)

        # Viewmodels
        ContainerService.register_type(SplashViewmodel)
        ContainerService.register_type(SettingsViewmodel)
        ContainerService.register_type(MeasureNameSelectViewmodel)
        ContainerService.register_type(MeasureDistanceViewmodel)
        ContainerService.register_type(SettingsViewmodel)

        # Services
        ContainerService.register_type(NetworkService)
        ContainerService.register_type(MqttService)

        # Sensors
        ContainerService.register_type(DistanceSensor)

    def _bind_views_viewmodels(self) -> None:
        self._bind_view_viewmodel(SplashView, SplashViewmodel)
        self._bind_view_viewmodel(SettingsView, SettingsViewmodel)
        self._bind_view_viewmodel(MeasureNameSelectView, MeasureNameSelectViewmodel)
        self._bind_view_viewmodel(MeasureDistanceView, MeasureDistanceViewmodel)

    def _bind_view_viewmodel(self, view_type: type, viewmodel_type: type) -> None:
        view: Optional[BaseView] = ContainerService.get_instance(view_type)
        viewmodel: Optional[BaseViewmodel] = ContainerService.get_instance(
            viewmodel_type
        )
        if view and viewmodel:
            view.bind_viewmodel(viewmodel)
            viewmodel.bind_view(view)

    async def _init_services_async(self) -> None:
        # Small delay to allow services/DI to settle
        await asyncio.sleep(0.1)

        logger.info("Initializing wifi...")
        if not await self._init_wifi_async():
            return
        logger.info("Syncing time...")
        if not await self._init_time():
            return
        logger.info("Initializing mqtt...")
        if not await self._init_mqtt_async():
            return

        await self._set_splash_message_async("Welcome!")
        await asyncio.sleep(0.5)
        NavigationService.navigate_to(MenuView)

    async def _init_wifi_async(self) -> bool:
        await self._set_splash_message_async("Connecting WiFi...")
        self._net_service = cast(
            NetworkService, ContainerService.get_instance(NetworkService)
        )
        try:
            connected = self._net_service.connect()
        except Exception as e:
            logger.critical(f"Error connecting to WiFi. {e}")
            await self._set_splash_message_async("WiFi error!")
            return False

        if not connected:
            await self._set_splash_message_async("Configure WiFi")
            logger.info("Starting web server...")
            try:
                # Fallback to captive portal / config server
                self._net_service.start_server()
            except Exception as e:
                logger.critical(f"Error starting web server. {e}")
                await self._set_splash_message_async("Web Server error!")
                return False
        return True

    async def _init_time(self) -> bool:
        await self._set_splash_message_async("Syncing time...")
        # NTP sync is fire-and-forget in this environment
        set_ntp_time()
        return True

    async def _init_mqtt_async(self) -> bool:
        await self._set_splash_message_async("Setting up services...")
        logger.info("Initializing MQTT...")
        try:
            self._mqtt_service = cast(
                MqttService, ContainerService.get_instance(MqttService)
            )
            self._mqtt_service.connect()
            # Subscribe to all Fermento topics
            self._mqtt_service.subscribe_topic("fermento/#")
        except OSError:
            logger.critical(f"Error connecting to MQTT broker.")
            await self._set_splash_message_async("Service error!")
            return False
        return True
