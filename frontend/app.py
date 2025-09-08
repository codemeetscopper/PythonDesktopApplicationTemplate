import asyncio
import sys
import time

from PySide6.QtWidgets import QApplication

from common.configuration.parser import ConfigurationManager
from common.logger import Logger
from frontend.context import ApplicationContext
from frontend.core import backend_worker
from frontend.mainwindow.mainwindow_c import MainWindow
from frontend.splash.splash_c import Splash


def run():
    app = QApplication(sys.argv)
    ApplicationContext.logger = Logger()
    ApplicationContext.backend_worker = backend_worker.get_instance()

    splash = Splash(ApplicationContext.name, ApplicationContext.version)
    splash.show()
    QApplication.processEvents()

    ApplicationContext.logger.info("Welcome!")
    _initialise_basic_settings()

    window = MainWindow()
    window.window_closing.connect(on_app_closing)
    window.show()
    splash.close()
    sys.exit(app.exec())

def on_app_closing():
    ApplicationContext.logger.info("Cleaning up...")
    if ApplicationContext.backend_worker is not None:
        ApplicationContext.backend_worker.shutdown()
    ApplicationContext.logger.info("Goodbye!")


def _initialise_basic_settings():
    ApplicationContext.settings = ConfigurationManager(ApplicationContext.config_path)
    QApplication.processEvents()
    ApplicationContext.backend_worker.start()

    def on_log_update(data):
        ApplicationContext.logger.info(data)
    ApplicationContext.backend_worker.on("backend_log_update", on_log_update)

    async def blocking_work(n):
        with ApplicationContext.backend_worker.token():
            for i in range(n):
                QApplication.processEvents()
                ApplicationContext.backend_worker.emit('backend_log_update', "Non blocking delay " + str(i))
                await asyncio.sleep(0.1)
                # time.sleep(1)

    ApplicationContext.backend_worker.run_async(blocking_work(100))
