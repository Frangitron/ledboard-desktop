from PySide6.QtWidgets import QWidget, QGridLayout

from ledboarddesktop.board_details_widget import BoardDetailsWidget
from ledboarddesktop.board_list.widget import BoardListWidget
from ledboarddesktop.components import Components


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board_list_widget = BoardListWidget()
        self.board_details_widget = BoardDetailsWidget()

        self.board_list_widget.itemSelectionChanged.connect(self._board_selected)

        layout = QGridLayout(self)
        layout.addWidget(self.board_list_widget, 0, 0)
        layout.addWidget(self.board_details_widget, 0, 1)

    def _board_selected(self):
        board = self.board_list_widget.selected_board()
        if board is not None:
            Components().board_communicator.request_board_details(board)
