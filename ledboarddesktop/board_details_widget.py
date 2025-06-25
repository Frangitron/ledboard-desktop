from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboarddesktop.components import Components
from ledboardlib import ListedBoard


class BoardDetailsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel()
        self.label.setWordWrap(True)

        layout = QGridLayout(self)
        layout.addWidget(self.label)

        board_communicator = Components().board_communicator
        board_communicator.boardDetailsAcquired.connect(self._details_acquired)
        board_communicator.boardDetailsAcquisitionFailed.connect(
            lambda message: self.label.setText(f"Communication busy/error\n\n{message}")
        )
        board_communicator.boardDetailsRequested.connect(
            lambda board: self.label.setText(f"Fetching details for {board.serial_port_name}...")
        )

        self.setFixedWidth(250)

    def _details_acquired(self, hardware_info: dict, hardware_configuration: dict):
        self.label.setText(
            "\n".join(f"{property}: {value}" for property, value in hardware_info.__dict__.items()) +
            "\n\n" +
            "\n".join(f"{property}: {value}" for property, value in hardware_configuration.__dict__.items())
        )
