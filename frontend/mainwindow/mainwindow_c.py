from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

from common.configuration.parser import ConfigurationManager
from frontend.mainwindow.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    window_closing = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._config = ConfigurationManager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.setWindowTitle("PySide6 MainWindow Example")

        setting = f"Setting is {self._config.get_value("sample_text_input").value}"
        label = QLabel(setting, self)
        layout = QVBoxLayout()
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def closeEvent(self, event):
        self.close()
        self.window_closing.emit()
        event.accept()