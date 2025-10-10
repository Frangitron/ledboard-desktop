from PySide6.QtCore import QTimer, QByteArray
from PySide6.QtGui import QPixmap, QPainter, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from ledboarddesktop.components import Components
from pyside6helpers import icons


class ScanWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.viewport = QLabel()
        self.button_start_stop = QPushButton("Start")
        self.button_start_stop.setIcon(icons.play_button())
        self.button_start_stop.clicked.connect(self._start_stop_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.viewport)
        layout.addWidget(self.button_start_stop)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_timeout)
        self._timer.start(int(1000 / 30))

    def _start_stop_clicked(self):
        scan_detection = Components().scan_detection
        if not scan_detection.is_running:
            started = scan_detection.start()
            if started:
                self.button_start_stop.setText("Stop")
                self.button_start_stop.setIcon(icons.stop())
        else:
            stopped = scan_detection.stop()
            if stopped:
                self.button_start_stop.setText("Start")
                self.button_start_stop.setIcon(icons.play_button())

    def _update_timeout(self):
        result = Components().scan_detection.get_latest_result()
        if result is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(result.frame_as_bytes), "JPG")
            if result.point is not None:
                painter = QPainter(pixmap)
                painter.setPen(Qt.red)
                painter.drawRect(result.point[0] - 2, result.point[1] - 2, 2, 2)
                painter.end()

            self.viewport.setPixmap(pixmap)
