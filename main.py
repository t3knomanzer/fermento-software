import sys

sys.path.insert(0, "lib/typing")

import config
from app.services import log

# Setup logging
log.LogServiceManager.initialize(level=log.DEBUG, max_files=config.LOG_MAX_FILES)
logger = log.LogServiceManager.get_logger(name=__name__)

from app.viewmodels.app import ApplicationViewmodel

app_viewmodel = None


def main():
    app_viewmodel = ApplicationViewmodel()
    app_viewmodel.start()


main()
