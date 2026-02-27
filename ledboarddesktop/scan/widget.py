import json
from importlib import resources

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

from ledboardlib import ListedBoard, BoardApi, InteropDataStore, SamplingPoint
from pyside6helpers import icons

from ledboarddesktop.components import Components
from ledboarddesktop.scan.viewport.widget import ScanViewport
from pyside6helpers.slider import Slider
from pyside6helpers.spinbox import SpinBox


class ScanWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_starting = False

        self.viewport = ScanViewport()
        self.viewport.detectionResultReceived.connect(self._detection_result_received)
        self.viewport.scanErrorOccurred.connect(self._set_start_button_start)
        self.viewport.setEnabled(False)

        self.range_first = SpinBox(name="first LED", minimum=0, maximum=10000)
        self.range_last = SpinBox(name="last LED", minimum=0, maximum=10000, value=360)
        self.interval = SpinBox(name="interval (ms)", minimum=1, maximum=10000, value=1500)
        self.button_scan = QPushButton("Scan")
        self.button_scan.clicked.connect(self._start_scan_clicked)

        self.button_start_stop = QPushButton("Start Camera")
        self.button_start_stop.setIcon(icons.play_button())
        self.button_start_stop.clicked.connect(self._start_stop_clicked)

        self.button_load_scan_data = QPushButton("Load scan data...")
        self.button_load_scan_data.setIcon(icons.file())
        self.button_load_scan_data.clicked.connect(self._load_scan_data_clicked)

        self.button_save_scan_data = QPushButton("Save scan data to interop")
        self.button_save_scan_data.setIcon(icons.diskette())
        self.button_save_scan_data.clicked.connect(self._save_scan_data_clicked)

        self.slider_blur = Slider(
            name="Blur",
            minimum=0, maximum=20, value=9,
            on_value_changed=self._options_changed
        )
        self.slider_average = Slider(
            name="Average frame count",
            minimum=1, maximum=20, value=4,
            on_value_changed=self._options_changed
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewport)
        layout.addWidget(self.slider_average)
        layout.addWidget(self.slider_blur)
        layout.addWidget(self.range_first)
        layout.addWidget(self.range_last)
        layout.addWidget(self.interval)
        layout.addWidget(self.button_scan)
        layout.addWidget(self.button_start_stop)
        layout.addWidget(self.button_load_scan_data)
        layout.addWidget(self.button_save_scan_data)

        self.timer: QTimer | None = None
        self.current_step: int | None = None
        self.board: ListedBoard | None = None
        self.api: BoardApi | None = None
        self.points: list[tuple[int, int]] | None = None

        self.latest_point_detected: tuple[int, int] | None = None
        self.viewport.detectionResultReceived.connect(lambda point: setattr(self, "latest_point_detected", point))

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
        self.button_start_stop.setText("Start Camera")
        self.button_start_stop.setIcon(icons.play_button())

    def _set_start_button_stop(self):
        self.button_start_stop.setEnabled(True)
        self.button_start_stop.setText("Stop Camera")
        self.button_start_stop.setIcon(icons.stop())

    def _start_scan_clicked(self):
        if self.timer is not None:
            self._stop()
        else:
            self._start()

    def _start(self):
        board_list_widget = Components().board_list_widget
        board_list_widget.setEnabled(False)
        self.board = board_list_widget.selected_board()
        if self.board is None:
            print("No board selected")
            return

        self.api = BoardApi(self.board.serial_port_name)

        self.current_step = self.range_first.value()
        self.points = []

        self.timer = QTimer()
        self.timer.timeout.connect(self._step1)
        self.timer.start(self.interval.value() * 2 / 3)

    def _step1(self):
        if self.current_step > self.range_last.value():
            self._stop()
            return

        self.button_scan.setText(f"Step {self.current_step}")
        self.current_step += 1

        if Components().scan_detection.is_running:
            parameters = self.api.get_control_parameters()
            parameters.single_led = self.current_step
            self.api.set_control_parameters(parameters)
            self.step2_timer = QTimer(self)
            self.step2_timer.timeout.connect(self._step2)
            self.step2_timer.start(self.interval.value() / 3)

    def _step2(self):
        if self.step2_timer is None:
            return

        self.step2_timer.stop()
        self.step2_timer.deleteLater()
        self.step2_timer = None

        if self.latest_point_detected is None:
            print("No detection result")
            return

        self.points.append(self.latest_point_detected)
        self.viewport.add_point(self.current_step, *self.latest_point_detected)

    def _stop(self):
        self.button_scan.setText("Scan")
        self.timer.stop()
        self.timer.deleteLater()

        self.timer = None
        self.current_step = None
        self.board = None
        self.api = None

        board_list_widget = Components().board_list_widget
        board_list_widget.setEnabled(True)

        with open("detec.json", "w") as file:
            json.dump(self.points, file, indent=2)
            self.points = None

    def _load_scan_data_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load scan data", "", "JSON files (*.json)")
        if not file_path:
            return

        with open(file_path, "r") as file:
            self.points = json.load(file)
            self.viewport.clear_detection_points()
            for i, point in enumerate(self.points):
                self.viewport.add_point(i, *point)

    def _save_scan_data_clicked(self):
        points = self.viewport.get_detection_points()

        interop_filepath = str(resources.files("ledboardtranslatoremulator.resources").joinpath("interop-data-elephanz.json"))
        interop_store = InteropDataStore(interop_filepath)
        for sampling_point in interop_store.data.sampling_points:
            sampling_point.x = int(points[sampling_point.index].x)
            sampling_point.y = int(points[sampling_point.index].y)
        interop_store._filepath = interop_filepath.replace(".json", "-quantized.json")
        interop_store.save()
