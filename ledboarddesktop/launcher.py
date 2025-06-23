from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from pyside6helpers import css
from pyside6helpers import icons
from pyside6helpers.main_window import MainWindow

from ledboarddesktop.board_detection.board_detector import BoardDetector
from ledboarddesktop.board_list.widget import BoardListWidget


class Launcher:
    def __init__(self):
        self._app = QApplication([])
        self._app.setApplicationName("LEDBoard")
        self._app.setOrganizationName("Frangitron")
        self._app.setApplicationDisplayName("LED Board")
        self._app.setWindowIcon(icons.print(Qt.black))
        css.load_onto(self._app)

        self._main_window = MainWindow()
        self._central_widget = BoardListWidget()
        self._main_window.setCentralWidget(self._central_widget)

        self._board_detector = BoardDetector()
        self._board_detector.boardsPolled.connect(self._central_widget.set_boards)
        self._app.aboutToQuit.connect(self._board_detector.stop)

    def run(self):
        self._main_window.show()
        self._board_detector.start()
        self._app.exec()
