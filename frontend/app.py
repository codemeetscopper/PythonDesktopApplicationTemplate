import asyncio
import logging
import sys
import time

from PySide6.QtWidgets import QApplication

import backend.backend_worker
from common.configuration.parser import ConfigurationManager
from common.logger import Logger
from frontend.mainwindow.mainwindow_c import MainWindow
from frontend.splash.splash_c import Splash


APP_NAME = "Python Desktop App Template"
APP_VERSION = "v0.1"
APP_CONFIG = "config/configuration.json"
APP_LOGGER = None
APP_SETTINGS = None

BACKEND_WORKER = None


def run():
    global APP_LOGGER, APP_SETTINGS

    app = QApplication(sys.argv)
    APP_LOGGER = Logger()

    splash = Splash(APP_NAME, APP_VERSION)
    splash.show()
    QApplication.processEvents()

    APP_LOGGER.info("Application started")
    _initialise_basic_settings()

    window = MainWindow()
    window.show()
    splash.close()

    sys.exit(app.exec())


def _initialise_basic_settings():
    global APP_CONFIG, APP_SETTINGS, BACKEND_WORKER
    APP_SETTINGS = ConfigurationManager(APP_CONFIG)
    QApplication.processEvents()

    BACKEND_WORKER = backend.backend_worker.get_instance()
    BACKEND_WORKER.start()

    async def blocking_work(n):
        with BACKEND_WORKER.token():
            for i in range(n):
                QApplication.processEvents()
                APP_LOGGER.info("Waiting for %d seconds..." % i)
                await asyncio.sleep(1)

    f = BACKEND_WORKER.run_async(blocking_work(5))

    # wait for all to finish
    f.result()

    BACKEND_WORKER.shutdown()
