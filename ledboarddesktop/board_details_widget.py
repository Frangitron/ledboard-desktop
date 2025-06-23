import serial
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboardlib.board_api import BoardApi


class BoardDetailsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board = None

        self.label = QLabel()

        layout = QGridLayout(self)
        layout.addWidget(self.label)

        self.setMinimumWidth(250)

    def set_board(self, board):
        self.board = board

        try:
            api = BoardApi(board.serial_port_name)
            configuration = api.get_configuration()

            self.label.setText(
                "\n".join(f"{property}: {value}" for property, value in board.hardware_info.__dict__.items()) +
                "\n\n" +
                "\n".join(f"{property}: {value}" for property, value in configuration.__dict__.items()
                          ))

        # FIXME raise a BoardApi exception ?
        except serial.serialutil.SerialException:
            self.label.setText("Board not available")
