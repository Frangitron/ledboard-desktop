from dataclasses import dataclass

from PySide6.QtCore import Qt

from pyside6helpers.annotated_form.types import ButtonType, IntegerSliderType, CheckBoxType, NoWidgetType, RadioEnumType
from pythonhelpers.dataclass_annotate import DataclassAnnotateMixin

from ledboardlib.color_mode import ColorMode
from ledboardlib import ControlParameters


@dataclass
class UiControlParameters(ControlParameters, DataclassAnnotateMixin):
    shutter: IntegerSliderType("Shutter", (0, 255))

    noise_octaves: IntegerSliderType("Noise octaves", (1, 6), group="Noise")

    noise_scale: IntegerSliderType("Noise scale", (1, 16), group="Noise scale")
    noise_scale_x: IntegerSliderType("Noise scale X", (0, 500), group="Noise scale")
    noise_scale_y: IntegerSliderType("Noise scale Y", (0, 500), group="Noise scale")

    noise_speed_x: IntegerSliderType("Noise speed X", (-200, 200), group="Noise speed")
    noise_speed_y: IntegerSliderType("Noise speed Y", (-200, 200), group="Noise speed")
    noise_speed_z: IntegerSliderType("Noise speed Z", (-200, 200), group="Noise speed")

    noise_min: IntegerSliderType("Noise min", (0, 1024), group="Noise clamping")
    noise_max: IntegerSliderType("Noise max", (0, 1024), group="Noise clamping")

    color_mode: RadioEnumType("Color mode", ColorMode, orientation=Qt.Horizontal, group="Color mode")

    noise_h: IntegerSliderType("Noise H", (0, 255), group="Noise color HSL")
    noise_s: IntegerSliderType("Noise S", (0, 255), group="Noise color HSL")
    noise_l: IntegerSliderType("Noise L", (0, 255), group="Noise color HSL")

    noise_r: IntegerSliderType("Noise R", (0, 255), group="Noise color RGB")
    noise_g: IntegerSliderType("Noise G", (0, 255), group="Noise color RGB")
    noise_b: IntegerSliderType("Noise B", (0, 255), group="Noise color RGB")

    runner_h: IntegerSliderType("Runner H", (0, 255), group="Runner color HSL")
    runner_s: IntegerSliderType("Runner S", (0, 255), group="Runner color HSL")
    runner_l: IntegerSliderType("Runner L", (0, 255), group="Runner color HSL")

    runner_r: IntegerSliderType("Runner R", (0, 255), group="Runner color RGB")
    runner_g: IntegerSliderType("Runner G", (0, 255), group="Runner color RGB")
    runner_b: IntegerSliderType("Runner B", (0, 255), group="Runner color RGB")

    runner_trigger: ButtonType("Runner trigger", (0, 1))
    are_colors_inverted: CheckBoxType("Are colors inverted?", (0, 1))
    is_noise_on: CheckBoxType("Is noise on?", (0, 1))

    # > 0: additive, < 0: multiply
    mask_x1: IntegerSliderType("Mask X1", (-255, 255), group="Mask X")
    mask_x2: IntegerSliderType("Mask X2", (-255, 255), group="Mask X")
    mask_y1: IntegerSliderType("Mask Y1", (-255, 255), group="Mask Y")
    mask_y2: IntegerSliderType("Mask Y2", (-255, 255), group="Mask Y")

    single_led: IntegerSliderType("Illuminate single LED", (-1, 32767), group="Scan & Debug")

    @staticmethod
    def from_base(base: ControlParameters):
        return UiControlParameters(**base.__dict__)
