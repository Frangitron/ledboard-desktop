from PySide6.QtWidgets import QWidget, QGridLayout


class ControlParametersWidget(QWidget):
    def __init__(self, parent=None):
        super(ControlParametersWidget, self).__init__(parent)

        layout = QGridLayout(self)

