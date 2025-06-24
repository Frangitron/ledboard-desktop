from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboardlib import ListedBoard


class ListedBoardWidget(QWidget):

    def __init__(self, board: ListedBoard, parent=None):
        super().__init__(parent)

        self.board = board
        self.label = QLabel()

        layout = QGridLayout(self)
        layout.addWidget(self.label)

        self.set_board(board)

    def set_board(self, board: ListedBoard):
        self.board = board

        if self.board.available:
            self.label.setText(f"{self.board.serial_port_name} - {self.board.hardware_info.name[:-1]}")
        else:
            self.label.setText(f"{self.board.serial_port_name} - Occupied")
