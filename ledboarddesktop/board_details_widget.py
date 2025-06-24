from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboarddesktop.components import Components
from ledboardlib import BoardApi, ListedBoard, UsbSerialException


class BoardDetailsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board = None

        self.label = QLabel()

        layout = QGridLayout(self)
        layout.addWidget(self.label)

        self.setMinimumWidth(250)

    def set_board(self, board: ListedBoard | None):
        self.board = board

        if board is None:
            self.label.setText("")
            return

        if not board.available:
            self.label.setText("Board not available...")
            return

        try:
            api = BoardApi(board.serial_port_name)
            configuration = api.get_configuration()

            self.label.setText(
                "\n".join(f"{property}: {value}" for property, value in board.hardware_info.__dict__.items()) +
                "\n\n" +
                "\n".join(f"{property}: {value}" for property, value in configuration.__dict__.items())
            )

        except UsbSerialException:
            Components().board_detector.request_board_refresh(board)
            self.label.setText("Usb Serial busy/error...")
