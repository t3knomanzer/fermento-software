import sys

import time


sys.path.insert(0, "./lib/typing")

from app.services import log

log.LogServiceManager.initialize(level=0, max_files=1)


from app.services.mqtt import MqttService
from camera import Camera, FrameSize, PixelFormat
from app.services.network import NetworkService


def init_wifi():
    print("Initializing WiFi...")
    _net_service = NetworkService()
    try:
        _net_service.connect()
    except Exception as e:
        print(f"Error connecting to WiFi. {e}")
        return False


class CameraPublisher:
    def __init__(self) -> None:
        print("Initializing camera publisher...")
        self._mqtt = MqttService(server="192.168.8.5", port=1883)
        self._mqtt.connect()

        self._cam = Camera(frame_size=FrameSize.VGA, pixel_format=PixelFormat.JPEG, init=False)
        self._cam.init()

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
    camera_publisher = CameraPublisher()

    for i in range(150):
        camera_publisher.capture()
        time.sleep(5)

    camera_publisher.deinit()


main()
