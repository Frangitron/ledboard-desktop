from PySide6.QtCore import QObject, Signal, QThread, Qt

from ledboardlib import ListedBoard, HardwareConfiguration, HardwareInfo

from ledboarddesktop.threaded_board_communication.woker import ThreadedBoardCommunicationWorker


class ThreadedBoardCommunicator(QObject):

    boardChanged = Signal(ListedBoard)
    boardDetailsRequested = Signal(ListedBoard)
    boardDetailsAcquired = Signal(HardwareInfo, HardwareConfiguration)
    boardDetailsAcquisitionFailed = Signal()
    boardRefreshRequested = Signal(ListedBoard)
    boardsListed = Signal(list)

    def __init__(self):
        super().__init__()

        self._worker = ThreadedBoardCommunicationWorker()
        self._worker.boardsListed.connect(self.boardsListed)
        self._worker.boardChanged.connect(self.boardChanged)
        self.boardRefreshRequested.connect(self._worker.request_board_refresh)
        self.boardDetailsRequested.connect(self._worker.request_board_details)
        self._worker.boardDetailsAcquired.connect(self.boardDetailsAcquired)
        self._worker.boardDetailsAcquisitionFailed.connect(self.boardDetailsAcquisitionFailed)

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

    def request_board_refresh(self, board: ListedBoard):
        self.boardRefreshRequested.emit(board)

    def request_board_details(self, board: ListedBoard):
        self.boardDetailsRequested.emit(board)
