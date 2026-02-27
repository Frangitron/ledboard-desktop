from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group

from ledboarddesktop.board_details_widget import BoardDetailsWidget
from ledboarddesktop.board_list.widget import BoardListWidget
from ledboarddesktop.components import Components
from ledboarddesktop.control_parameters.widget import ControlParametersWidget
from ledboarddesktop.firmware_selector_widget import FirmwareSelectorWidget
from ledboarddesktop.scan.widget import ScanWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)

        self.board_list_widget = BoardListWidget()
        self.board_list_widget.itemSelectionChanged.connect(self._board_selected)
        layout.addWidget(make_group(
            "Boards",
            [self.board_list_widget], fixed_width=400),
            0, 0
        )
        Components().board_list_widget = self.board_list_widget

        self.firmware_selector_widget = FirmwareSelectorWidget()
        layout.addWidget(make_group(
            "Firmware to upload",
            [self.firmware_selector_widget],
            fixed_width=400),
            1, 0
        )

        self.board_details_widget = BoardDetailsWidget()
        layout.addWidget(make_group(
            "Board details",
            [self.board_details_widget],
            fixed_width=400),
            2, 0
        )

        self.control_parameters_widget = ControlParametersWidget()
        layout.addWidget(make_group(
            "Control Parameters",
            [self.control_parameters_widget],
            with_checkbox=True),
            0, 1, 3, 1
        )

        self.scan_widget = ScanWidget()
        layout.addWidget(make_group(
            "Scan",
            [self.scan_widget],
            with_checkbox=True),
            0, 2, 3, 1
        )

        #layout.setColumnStretch(1, 50)
        #layout.setColumnStretch(2, 50)

    def _board_selected(self):
        board = self.board_list_widget.selected_board()
        self.control_parameters_widget.set_board(board)

        if board is None:
            self.board_details_widget.clear()
        else:
            Components().board_communicator.request_board_details(board)
