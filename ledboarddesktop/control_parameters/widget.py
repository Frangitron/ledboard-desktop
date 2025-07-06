from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from ledboarddesktop.components import Components
from ledboardlib import ListedBoard, ControlParameters
from ledboarddesktop.control_parameters.widget_maker import make_control_parameter_widget
from pyside6helpers.annotated_form import AnnotatedFormWidget


class ControlParametersWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel("Control parameters")
        self._layout.addWidget(self._label)

        self._form: AnnotatedFormWidget | None = None

        Components().board_communicator.boardControlParametersAcquired.connect(self.control_parameters_acquired)

    def clear(self):
        self._label.setVisible(True)
        self._label.setText("Control parameters")
        if self._form is not None:
            self._layout.removeWidget(self._form)
            self._form.deleteLater()
            self._form = None

    def set_board(self, board: ListedBoard | None):
        self.clear()

        if board is not None:
            self._label.setText("Waiting for response...")
            Components().board_communicator.request_board_control_parameters(board)

    @Slot(ControlParameters)
    def control_parameters_acquired(self, parameters: ControlParameters):
        self._form = make_control_parameter_widget(parameters)
        self._layout.addWidget(self._form)
        self._label.setVisible(False)
