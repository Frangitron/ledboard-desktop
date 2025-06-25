from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

from pyside6helpers import icons

from ledboardlib import ListedBoard

from ledboarddesktop.components import Components


class BoardListItemWidget(QWidget):

    def __init__(self, board: ListedBoard, parent=None):
        super().__init__(parent)

        self.board = board

        layout = QGridLayout(self)

        self.label = QLabel()
        layout.addWidget(self.label, 0, 0)
        layout.setColumnStretch(0, 1)

        self.button_reboot_to_bootloader = QPushButton()
        self.button_reboot_to_bootloader.setToolTip("Reboot")
        self.button_reboot_to_bootloader.setIcon(icons.refresh())
        self.button_reboot_to_bootloader.clicked.connect(self._reboot)
        layout.addWidget(self.button_reboot_to_bootloader, 0, 1)

        self.button_upload_firmware = QPushButton()
        self.button_upload_firmware.setToolTip("Upload firmware")
        self.button_upload_firmware.setIcon(icons.upload())
        self.button_upload_firmware.clicked.connect(self._upload_firmware)
        layout.addWidget(self.button_upload_firmware, 0, 2)

        self.button_upload_points = QPushButton()
        self.button_upload_points.setToolTip("Upload sampling points")
        self.button_upload_points.setIcon(icons.equalizer())
        self.button_upload_points.clicked.connect(self._upload_points)
        layout.addWidget(self.button_upload_points, 0, 3)

        self.set_board(board)

    def set_board(self, board: ListedBoard):
        self.board = board

        self.button_reboot_to_bootloader.setEnabled(self.board.available)
        self.button_upload_firmware.setEnabled(self.board.available)
        self.button_upload_points.setEnabled(self.board.available)

        if self.board.available:
            self.label.setText(f"{self.board.serial_port_name} - {self.board.hardware_info.name[:-1]}")
        else:
            self.label.setText(f"{self.board.serial_port_name} - Occupied")

    def _reboot(self):
        self.setEnabled(False)
        Components().board_communicator.request_board_reboot(self.board)

    def _upload_firmware(self):
        print(f"Uploading firmware: {self.board.serial_port_name}")

    def _upload_points(self):
        print(f"Uploading points: {self.board.serial_port_name}")
