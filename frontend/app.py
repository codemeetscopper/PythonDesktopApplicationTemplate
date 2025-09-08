import asyncio
import sys
import time

from PySide6.QtWidgets import QApplication

import frontend.core.backend_worker
from common.configuration.parser import ConfigurationManager
from common.logger import Logger
from frontend.mainwindow.mainwindow_c import MainWindow
from frontend.splash.splash_c import Splash


APP_NAME = "Python Desktop App Template"
APP_VERSION = "v0.1"
APP_CONFIG = "config/configuration.json"
APP_LOGGER = None
APP_SETTINGS = None

BACKEND_WORKER = frontend.core.backend_worker.get_instance()


def run():
    global APP_LOGGER, APP_SETTINGS,BACKEND_WORKER

    app = QApplication(sys.argv)
    APP_LOGGER = Logger()

    splash = Splash(APP_NAME, APP_VERSION)
    splash.show()
    QApplication.processEvents()

    APP_LOGGER.info("Application started")
    _initialise_basic_settings()

    window = MainWindow()
    window.window_closing.connect(on_app_closing)
    window.show()
    splash.close()
    sys.exit(app.exec())

def on_app_closing():
    global BACKEND_WORKER

    APP_LOGGER.info("Cleaning up...")
    if BACKEND_WORKER is not None:
        BACKEND_WORKER.shutdown()
    APP_LOGGER.info("Goodbye!")


def _initialise_basic_settings():
    global APP_CONFIG, APP_SETTINGS, BACKEND_WORKER
    APP_SETTINGS = ConfigurationManager(APP_CONFIG)
    QApplication.processEvents()

    def on_log_update(data):
        APP_LOGGER.info(data)

    BACKEND_WORKER.on("backend_log_update", on_log_update)
    BACKEND_WORKER.start()

    async def blocking_work(n):
        with BACKEND_WORKER.token():
            for i in range(n):
                QApplication.processEvents()
                BACKEND_WORKER.emit('backend_log_update', "Non blocking delay " + str(i))
                await asyncio.sleep(0.1)
                time.sleep(1)

    BACKEND_WORKER.run_async(blocking_work(100))
