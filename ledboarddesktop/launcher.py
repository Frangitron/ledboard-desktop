from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ledboarddesktop.central_widget import CentralWidget
from ledboarddesktop.components import Components
from pyside6helpers import css
from pyside6helpers import icons
from pyside6helpers.main_window import MainWindow

from ledboarddesktop.board_detection.board_detector import BoardDetector


class Launcher:
    def __init__(self):
        self._app = QApplication([])
        self._app.setApplicationName("LEDBoard")
        self._app.setOrganizationName("Frangitron")
        self._app.setApplicationDisplayName("LED Board")
        self._app.setWindowIcon(icons.print(Qt.black))
        css.load_onto(self._app)

        self._main_window = MainWindow()
        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)

        self._app.aboutToQuit.connect(Components().board_detector.stop)

    def run(self):
        self._main_window.show()
        Components().board_detector.start()
        self._app.exec()
