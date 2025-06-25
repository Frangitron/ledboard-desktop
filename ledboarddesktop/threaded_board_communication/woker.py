from PySide6.QtCore import QObject, Signal, Slot, QTimer

from ledboardlib import (
    BoardApi,
    BoardDetectionApi,
    HardwareConfiguration,
    HardwareInfo,
    ListedBoard,
    UsbSerialException,
)


class ThreadedBoardCommunicationWorker(QObject):

    boardChanged = Signal(ListedBoard)
    boardDetailsAcquired = Signal(HardwareInfo, HardwareConfiguration)
    boardDetailsAcquisitionFailed = Signal()
    boardsListed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_running = False

        self._detection_api = BoardDetectionApi()
        self._previous_boards: dict[str, ListedBoard] = dict()
        self._requested_for_refresh: list[str] = list()

        self._poll_timer : QTimer | None = None
        self._poll_interval = 1000

        self._is_polling = False
        self._suspend_polling = False

    def poll_forever(self):
        self._poll_timer = QTimer()
        self._poll_timer.timeout.connect(self._poll)
        self._poll_timer.setInterval(self._poll_interval)
        self._is_running = True
        self._poll_timer.start()
        self._poll()

    def stop(self):
        self._is_running = False
        if self._poll_timer:
            self._poll_timer.stop()

    def _poll(self):
        if self._suspend_polling:
            return

        self._is_polling = True

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
            self.boardsListed.emit(list(boards.values()))

        self._is_polling = False

    @Slot(ListedBoard)
    def request_board_refresh(self, board: ListedBoard):
        self._requested_for_refresh.append(board.serial_port_name)

    @Slot(ListedBoard)
    def request_board_details(self, board: ListedBoard):
        while self._is_polling:
            continue

        self._suspend_polling = True

        try:
            api = BoardApi(board.serial_port_name)
            hardware_info = api.get_hardware_info()
            hardware_configuration = api.get_configuration()
            self.boardDetailsAcquired.emit(hardware_info, hardware_configuration)

        except UsbSerialException:
            self.boardDetailsAcquisitionFailed.emit()

        finally:
            self._suspend_polling = False
