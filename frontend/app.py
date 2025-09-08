import logging
import sys

from PySide6.QtWidgets import QApplication

from common.configuration.parser import ConfigurationManager
from common.logger import Logger
from frontend.mainwindow.mainwindow_c import MainWindow
from frontend.splash.splash_c import Splash


APP_NAME = "Python Desktop App Template"
APP_VERSION = "v0.1"


def run():
    app = QApplication(sys.argv)
    logger = Logger()

    splash = Splash(APP_NAME, APP_VERSION)
    splash.show()
    QApplication.processEvents()

    logger.info("Application started")
    config = ConfigurationManager("config/configuration.json")

    window = MainWindow()
    window.show()
    splash.close()

    sys.exit(app.exec())
