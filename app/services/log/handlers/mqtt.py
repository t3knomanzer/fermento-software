from app.services.container import ContainerService
from app.services.log.handlers.base import BaseHandler
from app.services.mqtt import MqttService


class MQTTLogHandler(BaseHandler):
    def __init__(self, mqtt: MqttService):
        self._mqtt_service = mqtt

    def log(self, message: str, level: str, name: str):
        if not self._mqtt_service._is_connected:
            return

        try:
            self._mqtt_service.publish(
                "log",
                {
                    "name": name,
                    "level": level,
                    "message": message,
                },
                qos=0,
            )
        except Exception as e:
            # logger.error(f"Error publishing log message to MQTT: {e}")
            pass
