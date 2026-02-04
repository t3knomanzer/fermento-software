import sys

sys.path.insert(0, "src")

import config
from src.app.services import log

# Setup logging
log.LogServiceManager.initialize(level=log.DEBUG, max_files=config.LOG_MAX_FILES)

import src.hardware_setup
from src.app.screens.splash import SplashScreen
from src.lib.gui.core.ugui import Screen

logger = log.LogServiceManager.get_logger(name=__name__)


def main():
    logger.info("Starting app...")
    Screen.change(SplashScreen)


main()
