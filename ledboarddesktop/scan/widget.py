from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from pyside6helpers import icons

from ledboarddesktop.components import Components
from ledboarddesktop.scan.viewport.widget import ScanViewport
from pyside6helpers.slider import Slider


class ScanWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_starting = False

        self.viewport = ScanViewport()
        self.viewport.detectionResultReceived.connect(self._detection_result_received)
        self.viewport.scanErrorOccurred.connect(self._set_start_button_start)
        self.viewport.setEnabled(False)

        self.button_start_stop = QPushButton("Start")
        self.button_start_stop.setIcon(icons.play_button())
        self.button_start_stop.clicked.connect(self._start_stop_clicked)

        self.slider_blur = Slider(
            name="Blur",
            minimum=0, maximum=20,
            on_value_changed=self._options_changed
        )
        self.slider_average = Slider(
            name="Average frame count",
            minimum=1, maximum=20,
            on_value_changed=self._options_changed
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewport)
        layout.addWidget(self.slider_average)
        layout.addWidget(self.slider_blur)
        layout.addWidget(self.button_start_stop)

    def _detection_result_received(self):
        if self._is_starting:
            self._set_start_button_stop()
            self.viewport.setEnabled(True)
            self._is_starting = False

    def _options_changed(self, _):
        options = Components().scan_detection.get_options()
        options.blur_radius = self.slider_blur.value()
        options.average_frame_count = self.slider_average.value()
        Components().scan_detection.set_options(options)

    def _start_stop_clicked(self):
        scan_detection = Components().scan_detection
        if not scan_detection.is_running:
            if scan_detection.start():
                self._is_starting = True
                self._set_start_button_starting()
                self.viewport.start_viewport_update_timer()
        else:
            self.viewport.stop_viewport_update_timer()
            self.viewport.setEnabled(False)
            stopped = scan_detection.stop()
            self.viewport.clear_viewport()
            if stopped:
                self._set_start_button_start()

    def _set_start_button_starting(self):
        self.button_start_stop.setEnabled(False)
        self.button_start_stop.setText("Starting camera process")
        self.button_start_stop.setIcon(icons.more())

    def _set_start_button_start(self):
        self.button_start_stop.setEnabled(True)
        self.button_start_stop.setText("Start")
        self.button_start_stop.setIcon(icons.play_button())

    def _set_start_button_stop(self):
        self.button_start_stop.setEnabled(True)
        self.button_start_stop.setText("Stop")
        self.button_start_stop.setIcon(icons.stop())
