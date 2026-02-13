import sys

sys.path.insert(0, "lib/typing")

import config
from app.services.log.log import LogServiceManager
from app.services.log.handlers.console import ConsoleHandler

# Setup logging
LogServiceManager.initialize(level=config.LOG_LEVEL)
LogServiceManager.register_handler(ConsoleHandler())
logger = LogServiceManager.get_logger(name=__name__)

import hardware_setup
from app.viewmodels.app import ApplicationViewmodel


def main():
    logger.info("Application starting...")
    app_viewmodel = ApplicationViewmodel()
    app_viewmodel.start()


main()
