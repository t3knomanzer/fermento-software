from app.sensors.i2c_bus import I2CBus
from app.services.container import ContainerService
from app.services.log.log import LogServiceManager
import config

logger = LogServiceManager.get_logger(name=__name__)

import gc
import sys
from machine import I2C, Pin
import time
from drivers.ssd1306 import SSD1306_I2C as SSD

logger.info("Importing gui...")
from lib.gui.core.ugui import Display, Screen

logger.info("Creating SSD...")
oled_width = 128
oled_height = 64
ssd = None

retries = 3
while not ssd and retries > 0:
    try:
        gc.collect()
        i2c = I2C(0, sda=Pin(config.I2C_0_SDA_PIN), scl=Pin(config.I2C_0_SCL_PIN))
        ssd = SSD(oled_width, oled_height, i2c)
    except Exception as e:
        logger.error(f"({retries}) Error creating SSD. {e}")
        retries -= 1
        time.sleep(1)

if ssd is None:
    logger.critical("Couldn't create SSD.")
    sys.exit()

logger.info("Creating button pins...")
btn_nxt = Pin(config.INPUT_NXT_PIN, Pin.IN, Pin.PULL_UP)
btn_sel = Pin(config.INPUT_SEL_PIN, Pin.IN, Pin.PULL_UP)
btn_prev = None
btn_inc = None
btn_dec = None

logger.info("Creating Display object...")
display = Display(ssd, btn_nxt, btn_sel, btn_prev, btn_inc, btn_dec)
Screen.do_gc = False
