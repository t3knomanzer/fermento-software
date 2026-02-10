import asyncio
from datetime import datetime
import json
import random
import time
from app.services import log
import config
import machine
from app.utils.decorators import singleton
from lib.umqtt.simple import MQTTClient, hexlify

logger = log.LogServiceManager.get_logger(name=__name__)


class MqttService:
    def __init__(
        self,
        server: str = config.MQTT_SERVER,
        port: int = config.MQTT_PORT,
        topic_prefix: str = "fermento",
    ):
        self._topic_prefix = topic_prefix
        self._message_handlers = []
        self._topics = []
        self._is_connected = False
        self._device_id = hexlify(machine.unique_id()).decode()
        self.client = MQTTClient(client_id=self._device_id, server=server, port=port)
        self.client.set_callback(self._message_handler)

    def _get_topic(self, topic):
        return f"{self._topic_prefix}/{self._device_id}/{topic}"

    def _message_handler(self, topic, msg):
        for handler in self._message_handlers:
            handler(msg.decode(), topic.decode())

    def add_message_handler(self, handler):
        self._message_handlers.append(handler)

    def subscribe_topic(self, topic, qos=0):
        if self._is_connected:
            self._topics.append(topic)
            self.client.subscribe(topic, qos=qos)

    async def _check_msg_async(self):
        while self._is_connected:
            self.client.check_msg()
            await asyncio.sleep(0.5)

    def connect(self):
        try:
            self.client.connect(timeout=5000)
            self._is_connected = True
        except Exception as e:
            logger.critical(f"Error connecting to MQTT server: {e}")
            self._is_connected = False
            return

        for topic in self._topics:
            self.client.subscribe(topic)

        self._check_msg_task = asyncio.create_task(self._check_msg_async())

    def disconnect(self):
        self._is_connected = False
        self._check_msg_task.cancel()
        self.client.disconnect()

    def publish(self, topic, message={}, qos=0):
        if not self._is_connected:
            logger.warning("MQTT client not connected. Cannot publish message.")
            return

        if not isinstance(message, dict):
            logger.error("MQTT message must be a dictionary.")
            return

        message.update(
            {
                "device_id": self._device_id,
                "message_id": str(random.randint(0, 1000000)),
                "timestamp": datetime.now().isoformat(),
            }
        )

        try:
            str_message = json.dumps(message)
            self.client.publish(self._get_topic(topic), str_message, qos=qos)
        except Exception as e:
            logger.error(f"Error publishing MQTT message: {e}")
