from PySide6.QtCore import QObject, Signal, QThread, Qt

from ledboardlib import ListedBoard, HardwareConfiguration, HardwareInfo

from ledboarddesktop.threaded_board_communication.woker import ThreadedBoardCommunicationWorker


class ThreadedBoardCommunicator(QObject):
    """
    Handles multithreaded communication with boards through signals and slots.

    This class is a high-level interface to manage communication with boards, handling
    requests for details, reboot, refresh actions, and acquiring board updates. It uses
    PyQT's threading and signal-slot mechanisms to operate within a dedicated worker
    thread, ensuring smooth functionality in a multithreaded environment.

    Signals
    -------
    - boardChanged: Emitted when a board's parameters change.
    - boardDetailsAcquired: Emitted when board details (hardware info and configuration)
      are successfully acquired.
    - boardDetailsAcquisitionFailed: Emitted when acquiring board details fails, carrying
      an error message.
    - boardDetailsRequested: Emitted to request details for a specific board.
    - boardRebootRequested: Emitted to request a reboot for a specific board.
    - boardRebooted: Emitted when a board reboot is completed.
    - boardRefreshRequested: Emitted to request a data refresh for a specific board.
    - boardsListed: Emitted when the list of detected boards is updated.

    :ivar boardChanged: Signal emitted when a board's parameters change.
    :type boardChanged: Signal
    :ivar boardDetailsAcquired: Signal emitted when board details are acquired successfully.
    :type boardDetailsAcquired: Signal
    :ivar boardDetailsAcquisitionFailed: Signal emitted when acquiring board details fails.
    :type boardDetailsAcquisitionFailed: Signal
    :ivar boardDetailsRequested: Signal emitted when requesting details of a board.
    :type boardDetailsRequested: Signal
    :ivar boardRebootRequested: Signal emitted when requesting a board reboot.
    :type boardRebootRequested: Signal
    :ivar boardRebooted: Signal emitted when a board reboot completes.
    :type boardRebooted: Signal
    :ivar boardRefreshRequested: Signal emitted when requesting a board refresh.
    :type boardRefreshRequested: Signal
    :ivar boardsListed: Signal emitted when a new list of boards is available.
    :type boardsListed: Signal
    """

    boardChanged = Signal(ListedBoard)
    boardDetailsAcquired = Signal(HardwareInfo, HardwareConfiguration)
    boardDetailsAcquisitionFailed = Signal(str)
    boardDetailsRequested = Signal(ListedBoard)
    boardRebootRequested = Signal(ListedBoard)
    boardRebooted = Signal(ListedBoard)
    boardRefreshRequested = Signal(ListedBoard)
    boardsListed = Signal(list)
    firmwareUploadRequested = Signal(ListedBoard, str)

    def __init__(self):
        super().__init__()

        self._worker = ThreadedBoardCommunicationWorker()
        self._worker.boardChanged.connect(self.boardChanged)
        self._worker.boardDetailsAcquired.connect(self.boardDetailsAcquired)
        self._worker.boardDetailsAcquisitionFailed.connect(self.boardDetailsAcquisitionFailed)
        self._worker.boardsListed.connect(self.boardsListed)
        self._worker.boardRebooted.connect(self.boardRebooted)

        self.boardDetailsRequested.connect(self._worker.request_board_details)
        self.boardRebootRequested.connect(self._worker.request_reboot)
        self.boardRefreshRequested.connect(self._worker.request_board_refresh)
        self.firmwareUploadRequested.connect(self._worker.request_firmware_upload)

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

    def request_board_details(self, board: ListedBoard):
        self.boardDetailsRequested.emit(board)

    def request_board_reboot(self, board: ListedBoard):
        self.boardRebootRequested.emit(board)

    def request_board_refresh(self, board: ListedBoard):
        self.boardRefreshRequested.emit(board)

    def request_firmware_upload(self, board: ListedBoard, firmware_filepath: str):
        self.firmwareUploadRequested.emit(board, firmware_filepath)
