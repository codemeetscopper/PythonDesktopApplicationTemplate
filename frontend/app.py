from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys

from common.configuration.parser import ConfigurationManager


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._config = ConfigurationManager()

        self.setWindowTitle("PySide6 MainWindow Example")
        self.setGeometry(100, 100, 600, 400)

        label = QLabel("Hello, PySide6!", self)
        layout = QVBoxLayout()
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)