from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboarddesktop.components import Components


class BoardDetailsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        stretch = QWidget()
        layout.addWidget(stretch, 1, 0)
        layout.setRowStretch(1, 1)

        board_communicator = Components().board_communicator
        board_communicator.boardDetailsAcquired.connect(self._details_acquired)
        board_communicator.boardDetailsAcquisitionFailed.connect(
            lambda message: self.label.setText(f"Communication busy/error\n\n{message}")
        )
        board_communicator.boardDetailsRequested.connect(
            lambda board: self.label.setText(f"Fetching details for {board.serial_port_name}...")
        )

        self.setFixedWidth(300)

    def _details_acquired(self, hardware_info: dict, hardware_configuration: dict):
        self.label.setText(
            "\n".join(f"{property}: {value}" for property, value in hardware_info.__dict__.items()) +
            "\n\n" +
            "\n".join(f"{property}: {value}" for property, value in hardware_configuration.__dict__.items())
        )

    def clear(self):
        self.label.setText("")
