import sys

from PySide6.QtWidgets import QApplication

from common.configuration.parser import ConfigurationManager
from common.logger import Logger
from frontend.mainwindow.mainwindow_c import MainWindow
from frontend.splash.splash_c import Splash


def run():
    app = QApplication(sys.argv)
    logger = Logger()

    splash = Splash("Python Desktop App Template", "v0.1")
    splash.show()

    config = ConfigurationManager("config/configuration.json")

    # Simulate loading
    import time
    for i in range(101):
        splash.set_progress(i, )
        time.sleep(0.03)  # Simulate work

    window = MainWindow()
    window.show()
    splash.close()

    sys.exit(app.exec())