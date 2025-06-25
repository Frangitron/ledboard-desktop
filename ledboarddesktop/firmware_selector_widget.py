from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QFileDialog

from ledboarddesktop.components import Components


class FirmwareSelectorWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Firmware file path:")
        layout.addWidget(label, 0, 0)

        self.lineedit_filepath = QLineEdit()
        self.lineedit_filepath.setText(Components().settings.firmware_filepath)
        self.lineedit_filepath.textChanged.connect(self._update_settings)
        layout.addWidget(self.lineedit_filepath, 0, 1)

        self.button_browse = QPushButton("Browse...")
        self.button_browse.clicked.connect(self._browse)
        layout.addWidget(self.button_browse, 0, 2)

    def filepath(self) -> str:
        return self.lineedit_filepath.text()

    def set_filepath(self, filepath: str):
        self.lineedit_filepath.setText(filepath)

    def _update_settings(self):
        Components().settings.firmware_filepath = self.filepath()

    def _browse(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select firmware file",
            self.filepath(),
            "Firmware files (*.uf2);;All files (*.*)"
        )
        if filepath:
            self.set_filepath(filepath)
