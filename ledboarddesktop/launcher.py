from importlib.resources import files

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from pyside6helpers import css, resources
from pyside6helpers import icons
from pyside6helpers.main_window import MainWindow

from ledboarddesktop.central_widget import CentralWidget
from ledboarddesktop.components import Components


class Launcher:
    def __init__(self):
        Components().settings.load()

        self._app = QApplication([])
        self._app.setApplicationName("LEDBoard")
        self._app.setOrganizationName("Frangitron")
        self._app.setApplicationDisplayName("LED Board")
        self._app.setWindowIcon(icons.print(Qt.black))
        css.load_onto(self._app)

        self._main_window = MainWindow(
            logo_filepath=files('ledboarddesktop.resources').joinpath('frangitron-logo.png')
        )
        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)

        self._app.aboutToQuit.connect(Components().board_communicator.stop)
        self._app.aboutToQuit.connect(Components().settings.save)
        self._app.aboutToQuit.connect(Components().scan_detection.stop)

    def run(self):
        self._main_window.show()
        Components().board_communicator.start()
        self._app.exec()
