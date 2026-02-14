import asyncio
from typing import Optional, cast
from app.sensors.camera import CameraSensor
from app.sensors.co2 import CO2Sensor
from app.sensors.distance import DistanceSensor
from app.sensors.i2c_bus import I2CBus
from app.sensors.trh import TRHSensor
from app.services.log import log
from app.services.container import ContainerService
from app.services.mqtt import MqttService
from app.services.navigation import NavigationService
from app.services.network import NetworkService
from app.services.state import AppStateService
from app.services.timer import TimerService
from app.utils.time import setup_ntp_time
from app.viewmodels.base import BaseViewmodel
from app.viewmodels.measure_distance import MeasureDistanceViewmodel
from app.viewmodels.measure_name_select import MeasureNameSelectViewmodel
from app.viewmodels.settings import SettingsViewmodel
from app.viewmodels.splash import SplashViewmodel
from app.viewmodels.track_feeding_select import TrackFeedingSelectViewmodel
from app.viewmodels.track_fermentation import TrackFermentationViewmodel
from app.views.base import BaseView
from app.views.measure_distance import MeasureDistanceView
from app.views.measure_name_select import MeasureNameSelectView
from app.views.menu import MenuView
from app.views.settings import SettingsView
from app.views.splash import SplashView
from app.views.track_feeding_select import TrackFeedingSelectView
from app.views.track_fermentation import TrackFermentationView
import config
from lib.gui.core.ugui import Screen

logger = log.LogServiceManager.get_logger(name=__name__)


class ApplicationViewmodel(BaseViewmodel):
    def __init__(self):
        super().__init__()
        self._net_service: Optional[NetworkService] = None
        self._mqtt_service: Optional[MqttService] = None
        self._distance_sensor: Optional[DistanceSensor] = None
        self._i2c_bus: Optional[I2CBus] = None

    def start(self) -> None:
        self._register_types()
        self._init_sensors()
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
        logger.debug("Registering types...")
        # Views
        ContainerService.register_type(SplashView)
        ContainerService.register_type(MenuView)
        ContainerService.register_type(SettingsView)
        ContainerService.register_type(MeasureNameSelectView)
        ContainerService.register_type(MeasureDistanceView)
        ContainerService.register_type(TrackFeedingSelectView)
        ContainerService.register_type(TrackFermentationView)
        ContainerService.register_type(SettingsView)

        # Viewmodels
        ContainerService.register_type(SplashViewmodel)
        ContainerService.register_type(SettingsViewmodel)
        ContainerService.register_type(TrackFeedingSelectViewmodel)
        ContainerService.register_type(TrackFermentationViewmodel)
        ContainerService.register_type(MeasureNameSelectViewmodel)
        ContainerService.register_type(MeasureDistanceViewmodel)
        ContainerService.register_type(SettingsViewmodel)

        # Services
        ContainerService.register_type(AppStateService)
        ContainerService.register_type(NetworkService)
        ContainerService.register_type(MqttService)
        ContainerService.register_type(TimerService)
        ContainerService.register_type(I2CBus)

        # Sensors
        ContainerService.register_type(DistanceSensor)
        ContainerService.register_type(TRHSensor)
        ContainerService.register_type(CO2Sensor)
        ContainerService.register_type(CameraSensor)

    def _bind_views_viewmodels(self) -> None:
        logger.debug("Binding views and viewmodels...")
        self._bind_view_viewmodel(SplashView, SplashViewmodel)
        self._bind_view_viewmodel(SettingsView, SettingsViewmodel)
        self._bind_view_viewmodel(TrackFeedingSelectView, TrackFeedingSelectViewmodel)
        self._bind_view_viewmodel(TrackFermentationView, TrackFermentationViewmodel)
        self._bind_view_viewmodel(MeasureNameSelectView, MeasureNameSelectViewmodel)
        self._bind_view_viewmodel(MeasureDistanceView, MeasureDistanceViewmodel)

    def _bind_view_viewmodel(self, view_type: type, viewmodel_type: type) -> None:
        logger.debug(f"Binding {view_type.__name__} to {viewmodel_type.__name__}")
        view: Optional[BaseView] = ContainerService.get_instance(view_type)
        viewmodel: Optional[BaseViewmodel] = ContainerService.get_instance(viewmodel_type)
        if view and viewmodel:
            view.bind_viewmodel(viewmodel)
            viewmodel.bind_view(view)

    async def _init_services_async(self) -> None:
        logger.debug("Initializing services...")
        # Small delay to allow splash screen to render
        await asyncio.sleep(0.1)

        if not await self._init_wifi_async():
            return
        if not await self._init_time():
            return
        if not await self._init_mqtt_async():
            return

        await self._set_splash_message_async("Welcome!")
        await asyncio.sleep(0.5)
        NavigationService.navigate_to(MenuView)

    def _init_sensors(self) -> None:
        self._i2c_bus = ContainerService.get_instance(I2CBus)
        self._i2c_bus.start(
            id=config.I2C_0_ID, sda_pin=config.I2C_0_SDA_PIN, scl_pin=config.I2C_0_SCL_PIN
        )

    async def _init_wifi_async(self) -> bool:
        logger.info("Initializing WiFi...")
        await self._set_splash_message_async("Connecting WiFi...")
        self._net_service = cast(NetworkService, ContainerService.get_instance(NetworkService))
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
                logger.info(
                    f"Web server started connect to {config.WIFI_AP_SSID} password: {config.WIFI_AP_PASSWORD}"
                )
            except Exception as e:
                logger.critical(f"Error starting web server. {e}")
                await self._set_splash_message_async("Web Server error!")
                return False
        return True

    async def _init_time(self) -> bool:
        logger.info("Initializing NTP time...")
        await self._set_splash_message_async("Syncing time...")
        # NTP sync is fire-and-forget in this environment
        setup_ntp_time()
        return True

    async def _init_mqtt_async(self) -> bool:
        logger.info("Initializing MQTT...")
        await self._set_splash_message_async("Setting up services...")
        try:
            self._mqtt_service = cast(MqttService, ContainerService.get_instance(MqttService))
            self._mqtt_service.connect()
            # Subscribe to all Fermento topics
            self._mqtt_service.subscribe_topic("fermento/feeding_events/receive")
        except OSError:
            logger.critical(f"Error connecting to MQTT broker.")
            await self._set_splash_message_async("Service error!")
            return False
        return True
