import asyncio

import ujson
from app.schemas.feeding_event import FeedingEventSchema
from app.schemas.feeding_sample import FeedingSampleSchema
from app.screens.jar_name import JarNameScreen
from app.screens.settings import SettingsScreen
from app.screens.tracking_select import TrackingSelectScreen
from app.services.db import DBService
from app.services.log import LogServiceManager
from app.services.mqtt import MqttService
from app.utils import memory
from app.widgets.widgets.message_box import MessageBox
import config
from lib.gui.core.ugui import Screen, ssd

from lib.gui.core.writer import Writer
import lib.gui.fonts.arial10 as arial10
from lib.gui.widgets.buttons import Button

# Create logger
logger = LogServiceManager.get_logger(name=__name__)


class MainMenuScreen(Screen):
    NAV_JAR_NAME = "1"
    NAV_TRACKING_SELECT = "2"
    NAV_SETTINGS = "3"

    def __init__(self):
        super().__init__()
        self._db_service = DBService()
        self._writer = Writer(ssd, arial10, verbose=False)
        self._mqtt_service = MqttService()
        self._mqtt_service.add_message_handler(self._message_handler)

        # UI widgets
        btn_width = int(ssd.width / 1.5)
        btn_height = self._writer.height + 4

        # Measure button
        row = (ssd.height // 2) - btn_height // 2 - btn_height - 4
        col = ssd.width // 2 - btn_width // 2
        btn_01 = Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Measure",
            callback=self.navigate,
            args=(MainMenuScreen.NAV_JAR_NAME,),
        )

        # Track button
        row = ssd.height // 2 - btn_height // 2
        btn_02 = Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Track",
            callback=self.navigate,
            args=(MainMenuScreen.NAV_TRACKING_SELECT,),
        )

        # Settings button
        row = (ssd.height // 2) + btn_height // 2 + 4
        btn_03 = Button(
            self._writer,
            row=row,
            col=col,
            width=btn_width,
            height=btn_height,
            text="Settings",
            callback=self.navigate,
            args=(MainMenuScreen.NAV_SETTINGS,),
        )

    async def show_popup(self, message, duration=None):
        # Popup
        Screen.change(
            MessageBox,
            kwargs={"writer": self._writer, "message": message},
        )
        if duration:
            await asyncio.sleep(duration)
            Screen.back()
        else:
            await asyncio.sleep(0.01)

    def _message_handler(self, topic, message):
        """Handle incoming MQTT messages."""
        logger.debug(f"Received message on {topic}: {message}")
        if topic.decode() == config.TOPIC_MQTT_FEEDING_EVENTS_RECEIVE:
            asyncio.create_task(self.receive_events_async(message))

    async def request_events_async(self):
        # Retrieve feedings, this takes some time.
        logger.info("Retrieving feeding events...")
        await self.show_popup("Retrieving data...")

        try:
            self._mqtt_service.publish(config.TOPIC_MQTT_FEEDING_EVENTS_REQUEST, "", 1)
        except Exception as e:
            logger.error(f"Error requesting feeding events: {e}")

    async def receive_events_async(self, message):
        if message is None or not isinstance(message, bytes):
            logger.error("No feeding events received.")
            Screen.back()  # Close the popup
            await self.show_popup("Error retrieving feedings.", duration=2)
            return

        try:
            message = ujson.loads(message)
            feeding_events = [FeedingEventSchema.from_dict(event) for event in message]
            logger.info(f"Feeding events received {len(feeding_events)}")
        except Exception as e:
            logger.error(f"Error parsing JSON: {e}")
            Screen.back()  # Close the popup
            await self.show_popup("Error retrieving feedings.", duration=2)
            return

        if not len(feeding_events):
            logger.warning("No feedings found.")
            Screen.back()  # Close the popup
            await self.show_popup("No feedings found.", duration=2)
            return
        else:
            Screen.back()  # Close the popup
            Screen.change(TrackingSelectScreen, args=(feeding_events,))

    def navigate(self, button, arg):
        if arg == MainMenuScreen.NAV_JAR_NAME:
            Screen.change(JarNameScreen)
        elif arg == MainMenuScreen.NAV_TRACKING_SELECT:
            # Tracking needs to load the feedings from the DB.
            # We run it async since we need to update the UI
            asyncio.create_task(self.request_events_async())
        elif arg == MainMenuScreen.NAV_SETTINGS:
            Screen.change(SettingsScreen)
