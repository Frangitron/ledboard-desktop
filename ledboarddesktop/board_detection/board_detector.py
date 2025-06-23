from PySide6.QtCore import QObject, Signal, QThread

from ledboardlib.listed_board import ListedBoard

from ledboarddesktop.board_detection.woker import BoardDetectionWorker


class BoardDetector(QObject):

    boardsPolled = Signal(list)
    boardChanged = Signal(ListedBoard)

    def __init__(self):
        super().__init__()

        self._worker = BoardDetectionWorker()
        self._worker.boardsPolled.connect(self.boardsPolled)
        self._worker.boardChanged.connect(self.boardChanged)

        self._thread = QThread()
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.poll_forever)
        self._thread.finished.connect(self._thread.deleteLater)

    def start(self):
        if not self._thread.isRunning():
            self._thread.start()

    def stop(self):
        self._worker.stop()
        self._thread.quit()
        self._thread.wait()
