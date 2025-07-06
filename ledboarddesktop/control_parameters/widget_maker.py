from ledboarddesktop.control_parameters.annotated_dataclass import UiControlParameters
from pyside6helpers.annotated_form import AnnotatedFormWidget, AnnotatedFormWidgetMaker

from ledboardlib import ControlParameters


def make_control_parameter_widget(control_parameter: ControlParameters) -> AnnotatedFormWidget:
    ui_control_parameter = UiControlParameters.from_base(control_parameter)
    return AnnotatedFormWidgetMaker(ui_control_parameter).make_widget()
