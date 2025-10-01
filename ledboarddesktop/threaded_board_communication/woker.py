from PySide6.QtCore import QObject, Signal, Slot, QTimer

from ledboardlib import (
    BoardApi,
    BoardDetectionApi,
    HardwareConfiguration,
    HardwareInfo,
    ListedBoard,
    exceptions, ControlParameters,
)


class ThreadedBoardCommunicationWorker(QObject):
    """
    Manages threaded communication with connected boards by continuously polling and
    handling board-related requests, such as refreshing, rebooting, and acquiring details.

    This class is designed to detect and manage boards connected to the system in a
    thread-safe manner. It uses polling mechanisms and signals to communicate state
    changes and events related to connected boards. The functionality includes detecting
    board changes, responding to client requests such as rebooting or refreshing specific
    boards, and acquiring detailed board information.
    """

    poll_interval = 1000  # Don't need to be short, Windows takes time detecting ports when plugged/rebooted

    boardChanged = Signal(ListedBoard)
    boardControlParametersAcquired = Signal(ControlParameters)
    boardControlParametersSaved = Signal()
    boardDetailsAcquired = Signal(HardwareInfo, HardwareConfiguration)
    boardDetailsAcquisitionFailed = Signal(str)
    boardRebooted = Signal(ListedBoard)
    boardsListed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_running = False

        self._detection_api = BoardDetectionApi()
        self._previous_boards: dict[str, ListedBoard] = dict()
        self._requested_for_refresh: list[str] = list()
        self._waiting_for_reboot: list[str] = list()

        self._poll_timer : QTimer | None = None


        self._is_polling = False
        self._is_polling_suspended = False

    def poll_forever(self):
        self._poll_timer = QTimer()
        self._poll_timer.timeout.connect(self._poll)
        self._poll_timer.setInterval(self.poll_interval)
        self._is_running = True
        self._poll_timer.start()
        self._poll()

    def stop(self):
        self._is_running = False
        if self._poll_timer:
            self._poll_timer.stop()

    def _poll(self):
        if self._is_polling_suspended:
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

            if board.serial_port_name in self._waiting_for_reboot:
                self._waiting_for_reboot.remove(board.serial_port_name)
                self.boardRebooted.emit(board)

        if self._previous_boards.keys() != boards.keys():
            self._previous_boards = boards
            self.boardsListed.emit(list(boards.values()))

        self._is_polling = False

    @Slot(ListedBoard)
    def request_board_refresh(self, board: ListedBoard):
        self._requested_for_refresh.append(board.serial_port_name)

    @Slot(ListedBoard)
    def request_board_details(self, board: ListedBoard):
        self._suspend_polling()
        try:
            api = BoardApi(board.serial_port_name)
            hardware_info = api.get_hardware_info()
            hardware_configuration = api.get_configuration()
            self.boardDetailsAcquired.emit(hardware_info, hardware_configuration)

        except exceptions.UsbSerialException as e:
            self.boardDetailsAcquisitionFailed.emit(str(e))

        finally:
            self._restore_polling()

    @Slot(ListedBoard)
    def request_reboot(self, board: ListedBoard):
        self._suspend_polling()
        try:
            BoardApi(board.serial_port_name).reboot()
            self._waiting_for_reboot.append(board.serial_port_name)

        except exceptions.UsbSerialException as e:
            # TODO self.boardRebootRequestFailed.emit(str(e))
            print(e)

        finally:
            self._restore_polling()

    @Slot(ListedBoard, str)
    def request_firmware_upload(self, board: ListedBoard, firmware_filepath: str):
        self._suspend_polling()
        try:
            BoardApi(board.serial_port_name).upload_firmware(firmware_filepath)
            self._waiting_for_reboot.append(board.serial_port_name)

        except exceptions.UsbSerialException as e:
            # TODO self.boardFirmwareUploadRequestFailed.emit(str(e))
            print(e)

        finally:
            self._restore_polling()

    @Slot(ListedBoard)
    def request_board_control_parameters(self, board: ListedBoard):
        self._suspend_polling()
        try:
            control_parameters = BoardApi(board.serial_port_name).get_control_parameters()
            self.boardControlParametersAcquired.emit(control_parameters)

        except exceptions.UsbSerialException as e:
            # TODO self.boardFirmwareUploadRequestFailed.emit(str(e))
            print(e)

        finally:
            self._restore_polling()

    @Slot(ListedBoard, ControlParameters)
    def set_control_parameters(self, board: ListedBoard, parameters: ControlParameters):
        self._suspend_polling()
        try:
            BoardApi(board.serial_port_name).set_control_parameters(parameters)

        except exceptions.UsbSerialException as e:
            # TODO self.boardFirmwareUploadRequestFailed.emit(str(e))
            print(e)

        finally:
            self._restore_polling()

    @Slot(ListedBoard)
    def request_save_parameters(self, board: ListedBoard):
        self._suspend_polling()
        try:
            BoardApi(board.serial_port_name).save_control_parameters()
            self.boardControlParametersSaved.emit()

        except exceptions.UsbSerialException as e:
            # TODO self.boardFirmwareUploadRequestFailed.emit(str(e))
            print(e)

        finally:
            self._restore_polling()

    def _suspend_polling(self):
        while self._is_polling:
            continue

        self._is_polling_suspended = True

    def _restore_polling(self):
        self._is_polling_suspended = False
