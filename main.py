import sys

sys.path.insert(0, "lib/typing")

import config
from app.services import log

# Setup logging
log.LogServiceManager.initialize(level=config.LOG_LEVEL, max_files=config.LOG_MAX_FILES)
logger = log.LogServiceManager.get_logger(name=__name__)

import hardware_setup
from app.viewmodels.app import ApplicationViewmodel


def main():
    logger.info("Application starting...")
    app_viewmodel = ApplicationViewmodel()
    app_viewmodel.start()


main()
