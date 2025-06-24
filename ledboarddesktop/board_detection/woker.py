from PySide6.QtCore import QObject, Signal, QThread

from ledboardlib import BoardDetectionApi, ListedBoard


class BoardDetectionWorker(QObject):

    boardsPolled = Signal(list)
    boardChanged = Signal(ListedBoard)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_running = False

        self._detection_api = BoardDetectionApi()
        self._previous_boards: dict[str, ListedBoard] = dict()

    def poll_forever(self):
        self._is_running = True

        while self._is_running:
            self._poll()
            QThread.currentThread().msleep(1000)

    def stop(self):
        self._is_running = False

    def _poll(self):
        boards = {board.serial_port_name: board for board in self._detection_api.list_boards()}

        for board in boards.values():
            if board.serial_port_name not in self._previous_boards:
                continue

            if board.available != self._previous_boards[board.serial_port_name].available:
                self._previous_boards[board.serial_port_name] = board
                self.boardChanged.emit(board)

        if self._previous_boards.keys() != boards.keys():
            self._previous_boards = boards
            self.boardsPolled.emit(list(boards.values()))
