from PySide6.QtCore import QObject, Signal, Slot, QTimer, Qt

from ledboardlib import BoardDetectionApi, ListedBoard


class BoardDetectionWorker(QObject):

    boardsPolled = Signal(list)
    boardChanged = Signal(ListedBoard)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_running = False

        self._detection_api = BoardDetectionApi()
        self._previous_boards: dict[str, ListedBoard] = dict()
        self._requested_for_refresh: list[str] = list()

        self._timer : QTimer | None = None

    def poll_forever(self):
        self._timer = QTimer()
        self._timer.timeout.connect(self._poll)
        self._timer.setInterval(1000)
        self._is_running = True
        self._timer.start()
        self._poll()

    def stop(self):
        self._is_running = False
        if self._timer:
            self._timer.stop()

    def _poll(self):
        boards = {board.serial_port_name: board for board in self._detection_api.list_boards()}

        for board in boards.values():
            if board.serial_port_name not in self._previous_boards:
                continue

            if board.available != self._previous_boards[board.serial_port_name].available:
                self._previous_boards[board.serial_port_name] = board
                self.boardChanged.emit(board)

            if board.serial_port_name in self._requested_for_refresh:
                self._requested_for_refresh.remove(board.serial_port_name)
                self.boardChanged.emit(board)

        if self._previous_boards.keys() != boards.keys():
            self._previous_boards = boards
            self.boardsPolled.emit(list(boards.values()))

    @Slot(ListedBoard)
    def request_board_refresh(self, board: ListedBoard):
        self._requested_for_refresh.append(board.serial_port_name)
