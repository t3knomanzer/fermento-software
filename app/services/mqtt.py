import asyncio
import json
import random
import time
import machine
from lib.umqtt.simple import MQTTClient, hexlify


class MqttService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._device_id = hexlify(machine.unique_id()).decode()
        self._message_handlers = []
        self._is_connected = False
        self.client = MQTTClient(
            client_id=self._device_id, server="192.168.8.5", port=1883
        )
        self.client.set_callback(self.message_handler)

    def message_handler(self, topic, msg):
        print(topic.decode(), msg.decode())
        for handler in self._message_handlers:
            handler(topic, msg)

    def add_message_handler(self, handler):
        self._message_handlers.append(handler)

    def subscribe_topic(self, topic, qos=0):
        self.client.subscribe(topic, qos=qos)

    async def check_msg_async(self):
        while self._is_connected:
            result = self.client.check_msg()
            # if result:
            #     for handler in self._message_handlers:
            #         try:
            #             handler(result)
            #         except Exception as e:
            #             print(f"Error in MQTT message handler: {e}")
            await asyncio.sleep(0.1)

    def connect(self):
        self.client.connect()
        self._is_connected = True
        self._check_msg_task = asyncio.create_task(self.check_msg_async())

    def disconnect(self):
        self._is_connected = False
        self._check_msg_task.cancel()
        self.client.disconnect()

    def publish(self, topic, message, qos=0):
        if isinstance(message, dict):
            message.update(
                {
                    "schema": (1, 0, 0),
                    "device_id": self._device_id,
                    "message_id": str(random.randint(0, 1000000)),
                    "timestamp": str(time.time()),
                }
            )
            str_message = json.dumps(message)
        else:
            str_message = str(message)

        print(f"Publishing to topic {topic}: {str_message}")
        self.client.publish(topic, str_message, qos=qos)
