import os.path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QScrollArea

from pyside6helpers import icons, resources
from pyside6helpers.annotated_form import AnnotatedFormWidget
from pyside6helpers.message_box import confirmation_box

from ledboardlib import ListedBoard, ControlParameters, InteropDataStore

from ledboarddesktop.components import Components
from ledboarddesktop.control_parameters.annotated_dataclass import UiControlParameters
from ledboarddesktop.control_parameters.widget_maker import make_control_parameter_widget


class ControlParametersWidget(QWidget):

    _interop_filepath = "C:/Users/Ourson/PROJETS/ledboard/ledboard-translator-emulator/ledboardtranslatoremulator/resources/interop-data-elephanz.json"

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

        self._button_restore_from_emulator = QPushButton("Restore from emulator default values")
        self._button_restore_from_emulator.setIcon(icons.login())
        self._button_restore_from_emulator.clicked.connect(self._restore_defaults_from_emulator)
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._label, 0, 0, 1, 3)
        self._layout.addWidget(self._scroll_area, 1, 0, 1, 3)
        self._layout.addWidget(self._button_save_to_board_defaults, 2, 0)
        self._layout.addWidget(self._button_save_to_emulator, 2, 1)
        self._layout.addWidget(self._button_restore_from_emulator, 2, 2)

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

        interop_store = InteropDataStore(self._interop_filepath)
        interop_store.data.default_control_parameters = self._form.value()
        interop_store.save()

    def _restore_defaults_from_emulator(self):
        if self._form is None:
            return

        if not confirmation_box([
            'This will load default values stored in emulator data.',
            'Make sure to click "Save as board default values" if you want to save them to the actual board.',
            'Do you want to continue ?'
        ]):
            return


        interop_store = InteropDataStore(self._interop_filepath)
        interop_data = interop_store.data
        if interop_data.default_control_parameters is None:
            self._label.setText("No default values stored in emulator data")
        else:
            self.control_parameters_acquired(interop_data.default_control_parameters)

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
