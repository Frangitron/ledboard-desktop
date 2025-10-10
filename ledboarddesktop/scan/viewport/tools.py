from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSpinBox

from pyside6helpers import icons
from pyside6helpers.frame import make_h_line


class ScanViewportTools(QWidget):
    fitClicked = Signal()
    maskEditingChanged = Signal(bool)
    maskResetClicked = Signal()
    maskToggleVisible = Signal(bool)
    saveScanEditsClicked = Signal()
    assignSegmentIndex = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        #
        # Widgets
        self.button_fit_viewport = QPushButton("Fit view")
        self.button_fit_viewport.setIcon(icons.resize())
        self.button_fit_viewport.clicked.connect(self.fitClicked)

        self.button_mask_edit = QPushButton("Edit mask")
        self.button_mask_edit.setToolTip("Masking")
        self.button_mask_edit.setIcon(icons.screenshot())
        self.button_mask_edit.setCheckable(True)

        self.button_mask_toggle_visible = QPushButton("Mask visibility")
        self.button_mask_toggle_visible.setIcon(icons.vision())
        self.button_mask_toggle_visible.setCheckable(True)
        self.button_mask_toggle_visible.setChecked(True)
        self.button_mask_toggle_visible.toggled.connect(self._mask_toggle_visible)

        self.button_mask_reset = QPushButton("Reset mask")
        self.button_mask_reset.setToolTip("Masking")
        self.button_mask_reset.setIcon(icons.trash())

        self.button_save_scan_edits = QPushButton("Save edits")
        self.button_save_scan_edits.setToolTip("Save moved detected points, assigned segments")
        self.button_save_scan_edits.setIcon(icons.diskette())

        self.spin_segment_index = QSpinBox()
        self.spin_segment_index.setRange(-1, 4)
        self.button_assign_segment_index = QPushButton("Assign segment")
        self.button_assign_segment_index.setIcon(icons.equalizer())
        self.button_assign_segment_index.setToolTip("Assigns segment index to selected detection points")
        self.button_assign_segment_index.clicked.connect(self._assign_segment_index)

        #
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button_fit_viewport)

        layout.addWidget(make_h_line())
        layout.addWidget(self.button_mask_edit)
        layout.addWidget(self.button_mask_reset)
        layout.addWidget(self.button_mask_toggle_visible)

        layout.addWidget(make_h_line())
        layout.addWidget(self.spin_segment_index)
        layout.addWidget(self.button_assign_segment_index)

        layout.addWidget(make_h_line())
        layout.addWidget(self.button_save_scan_edits)

        layout.addWidget(QWidget())
        layout.setStretch(layout.count() - 1, 100)

        #
        # Signals
        self.button_mask_edit.clicked.connect(self.maskEditingChanged)
        self.button_mask_reset.clicked.connect(self.maskResetClicked)
        self.button_save_scan_edits.clicked.connect(self.saveScanEditsClicked)

    def _mask_toggle_visible(self):
        checked = self.button_mask_toggle_visible.isChecked()
        self.button_mask_toggle_visible.setIcon(icons.vision() if checked else icons.vision_stroked())
        self.maskToggleVisible.emit(checked)

    def _assign_segment_index(self):
        self.assignSegmentIndex.emit(self.spin_segment_index.value())
