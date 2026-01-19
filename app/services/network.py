import time
import network

from app.services.wifi_manager import WifiManager

import config


class NetworkService:
    def __init__(self):
        self._wm = WifiManager(ssid="Fermento", password="123456789", reboot=True)

    def start_server(self):
        self._wm.web_server()

    def connect(self):
        return self._wm.connect()
