from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from pyside6helpers import icons

from ledboarddesktop.components import Components
from ledboarddesktop.scan.viewport.widget import ScanViewport


class ScanWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.viewport = ScanViewport()
        self.button_start_stop = QPushButton("Start")
        self.button_start_stop.setIcon(icons.play_button())
        self.button_start_stop.clicked.connect(self._start_stop_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewport)
        layout.addWidget(self.button_start_stop)

    def _start_stop_clicked(self):
        scan_detection = Components().scan_detection
        if not scan_detection.is_running:
            started = scan_detection.start()
            if started:
                self.button_start_stop.setText("Stop")
                self.button_start_stop.setIcon(icons.stop())
                self.viewport.start_viewport_update_timer()
        else:
            self.viewport.stop_viewport_update_timer()
            stopped = scan_detection.stop()
            if stopped:
                self.button_start_stop.setText("Start")
                self.button_start_stop.setIcon(icons.play_button())
