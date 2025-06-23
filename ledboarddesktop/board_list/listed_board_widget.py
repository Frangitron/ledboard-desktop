from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboardlib.listed_board import ListedBoard


class ListedBoardWidget(QWidget):

    def __init__(self, listed_board=ListedBoard, parent=None):
        super().__init__(parent)

        self.board = listed_board
        if self.board.available:
            label = f"{self.board.serial_port_name} - {self.board.hardware_info.name[:-1]}"
        else:
            label = f"{self.board.serial_port_name} - Occupied"

        self.label = QLabel(label)

        layout = QGridLayout(self)
        layout.addWidget(self.label)
