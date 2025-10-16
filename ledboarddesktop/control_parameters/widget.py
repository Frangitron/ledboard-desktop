import os.path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QScrollArea

from pyside6helpers import icons
from pyside6helpers.annotated_form import AnnotatedFormWidget

from ledboardlib import ListedBoard, ControlParameters, InteropDataStore

from ledboarddesktop.components import Components
from ledboarddesktop.control_parameters.annotated_dataclass import UiControlParameters
from ledboarddesktop.control_parameters.widget_maker import make_control_parameter_widget


class ControlParametersWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # FIXME store that info elsewhere ?
        self._selected_board: ListedBoard | None = None

        self._label = QLabel("No board selected")
        self._form: AnnotatedFormWidget[UiControlParameters] | None = None
        self._button_save_to_board_defaults = QPushButton("Save as board default values")
        self._button_save_to_board_defaults.setIcon(icons.diskette())
        self._button_save_to_board_defaults.clicked.connect(
            lambda: Components().board_communicator.request_save_parameters(
                self._selected_board
            )
        )
        self._button_save_to_emulator = QPushButton("Save as emulator default values")
        self._button_save_to_emulator.setIcon(icons.laptop())
        self._button_save_to_emulator.clicked.connect(self._save_to_emulator_defaults)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._label, 0, 0, 1, 2)
        self._layout.addWidget(self._scroll_area, 1, 0, 1, 2)
        self._layout.addWidget(self._button_save_to_board_defaults, 2, 0)
        self._layout.addWidget(self._button_save_to_emulator, 2, 1)

        Components().board_communicator.boardControlParametersAcquired.connect(self.control_parameters_acquired)

    def clear(self):
        self._label.setVisible(True)
        self._label.setText("No board selected")
        if self._form is not None:
            self._scroll_area.setWidget(None)
            self._form.deleteLater()
            self._form = None

    def set_board(self, board: ListedBoard | None):
        self.clear()

        self._selected_board = board

        if board is not None:
            self._label.setText("Waiting for response...")
            Components().board_communicator.request_board_control_parameters(board)

    def _save_to_emulator_defaults(self):
        if self._form is None:
            return

        interop_store = InteropDataStore(
            "C:/Users/Ourson/PROJETS/ledboard/ledboard-translator-emulator/ledboardtranslatoremulator/resources/interop-data-melinerion.json"
        )
        interop_store.data.default_control_parameters = self._form.value()
        interop_store.save()

    @Slot(ControlParameters)
    def control_parameters_acquired(self, parameters: ControlParameters):
        self._form = make_control_parameter_widget(parameters)
        self._form.valueChanged.connect(
            lambda parameters_ : Components().board_communicator.set_control_parameters(
                self._selected_board,
                parameters_
            )
        )
        self._scroll_area.setWidget(self._form)
        self._label.setVisible(False)
