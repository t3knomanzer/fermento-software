from app.services.log.log import LogServiceManager
from app.services.wifi import WifiService

import config

# Create logger
logger = LogServiceManager.get_logger(name=__name__)


class NetworkService:
    def __init__(self):
        self._wm = WifiService(
            ssid=config.WIFI_AP_SSID, password=config.WIFI_AP_PASSWORD, reboot=True
        )

    def start_server(self):
        self._wm.web_server()

    def connect(self):
        return self._wm.connect()
