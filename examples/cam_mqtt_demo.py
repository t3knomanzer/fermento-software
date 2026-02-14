import sys

import time

import network


sys.path.insert(0, "./lib/typing")

from app.services.mqtt import MqttService
from camera import Camera, FrameSize, PixelFormat


def init_wifi():
    print("Initializing WiFi...")
    # WLAN config
    ssid = "YourSSID"
    password = "YourPassword"

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        time.sleep(1)
        print(".", end="")

    print(f"\nConnected! IP: {station.ifconfig()[0]}. Open this IP in your browser")


class CameraPublisher:
    def __init__(self) -> None:
        self._mqtt = MqttService(server="192.168.8.10", port=1883)
        self._cam = Camera(frame_size=FrameSize.VGA, pixel_format=PixelFormat.JPEG, init=False)

    def init(self) -> bool:
        print("Connecting to MQTT......")
        if not self._mqtt.connect():
            return False

        print("Initializing camera...")
        self._cam.init()
        return True

    def capture(self):
        print("Capturing image...")
        frame = self._cam.capture()

        if not frame:
            print("Failed to capture image")
            self._cam.deinit()
            return

        self.publish(frame)
        self._cam.free_buffer()

    def publish(self, frame):
        print("Publishing image...")
        self._mqtt.publish(topic=f"image", message=bytes(frame), qos=0)

    def deinit(self):
        print("Deinitializing camera publisher...")
        self._mqtt.disconnect()
        self._cam.deinit()


def main():
    init_wifi()

    time.sleep(2)

    camera_publisher = CameraPublisher()
    if not camera_publisher.init():
        print("Failed to connect to MQTT server")
        return

    for i in range(150):
        camera_publisher.capture()
        time.sleep(5)

    camera_publisher.deinit()


main()
