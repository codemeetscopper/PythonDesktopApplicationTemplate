import sys
from PySide6.QtWidgets import QApplication
from common.configuration.parser import ConfigurationManager
from frontend.app import MainWindow

def main():
    app = QApplication(sys.argv)
    config = ConfigurationManager("config/configuration.json")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()