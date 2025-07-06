from dataclasses import dataclass

from pyside6helpers.annotated_form.types import ButtonType, IntegerSliderType, CheckBoxType
from pythonhelpers.dataclass_annotate import DataclassAnnotateMixin

from ledboardlib import ControlParameters


@dataclass
class UiControlParameters(ControlParameters, DataclassAnnotateMixin):
    noise_octaves: IntegerSliderType("Noise octaves", (1, 6))
    noise_scale: IntegerSliderType("Noise scale", (1, 16))

    noise_scale_x: IntegerSliderType("Noise scale X", (0, 500))
    noise_scale_y: IntegerSliderType("Noise scale Y", (0, 500))

    noise_speed_x: IntegerSliderType("Noise speed X", (-200, 200))
    noise_speed_y: IntegerSliderType("Noise speed Y", (-200, 200))
    noise_speed_z: IntegerSliderType("Noise speed Z", (-200, 200))

    noise_min: IntegerSliderType("Noise min", (0, 1024))
    noise_max: IntegerSliderType("Noise max", (0, 1024))

    noise_r: IntegerSliderType("Noise R", (0, 255))
    noise_g: IntegerSliderType("Noise G", (0, 255))
    noise_b: IntegerSliderType("Noise B", (0, 255))

    runner_r: IntegerSliderType("Runner R", (0, 255))
    runner_g: IntegerSliderType("Runner G", (0, 255))
    runner_b: IntegerSliderType("Runner B", (0, 255))

    runner_trigger: ButtonType("Runner trigger", (0, 1))
    are_colors_inverted: CheckBoxType("Are colors inverted?", (0, 1))
    is_noise_on: CheckBoxType("Is noise on?", (0, 1))

    # > 0: additive, < 0: multiply
    mask_x1: IntegerSliderType("Mask X1", (-255, 255))
    mask_x2: IntegerSliderType("Mask X2", (-255, 255))
    mask_y1: IntegerSliderType("Mask Y1", (-255, 255))
    mask_y2: IntegerSliderType("Mask Y2", (-255, 255))

    bat_low: CheckBoxType("Bat low", (0, 1)) = 0
    bat_1_bar: CheckBoxType("Bat 1 bar", (0, 1)) = 0

    @staticmethod
    def from_base(base: ControlParameters):
        return UiControlParameters(**base.__dict__)
