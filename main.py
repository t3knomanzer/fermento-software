import sys

sys.path.insert(0, "src")

import config
from app.services import log

# Setup logging
log.LogServiceManager.initialize(level=log.DEBUG, max_files=config.LOG_MAX_FILES)
logger = log.LogServiceManager.get_logger(name=__name__)

import hardware_setup
from typing import cast
from app.viewmodels.app import ApplicationViewmodel

app_viewmodel = None


def main():
    logger.info("Starting app...")
    app_viewmodel = ApplicationViewmodel()
    app_viewmodel.start()


main()
