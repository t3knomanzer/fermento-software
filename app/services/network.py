import network

import config


class NetworkService:
    def __init__(self):
        pass

    def connect(self):
        print("Connecting to WiFi...")
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
        print("Connected")
