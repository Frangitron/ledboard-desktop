from PySide6.QtWidgets import QWidget, QGridLayout

from ledboarddesktop.board_details_widget import BoardDetailsWidget
from ledboarddesktop.board_list.widget import BoardListWidget
from ledboarddesktop.components import Components
from ledboarddesktop.firmware_selector_widget import FirmwareSelectorWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)

        self.board_details_widget = BoardDetailsWidget()
        layout.addWidget(self.board_details_widget, 0, 1)

        self.board_list_widget = BoardListWidget()
        self.board_list_widget.itemSelectionChanged.connect(self._board_selected)
        layout.addWidget(self.board_list_widget, 0, 0)

        self.firmware_selector_widget = FirmwareSelectorWidget()
        layout.addWidget(self.firmware_selector_widget, 1, 0, 1, 2)

    def _board_selected(self):
        board = self.board_list_widget.selected_board()

        if board is None:
            self.board_details_widget.clear()
        else:
            Components().board_communicator.request_board_details(board)
