from dataclasses import dataclass

from pyside6helpers.annotated_form.types import ButtonType, IntegerSliderType, CheckBoxType
from pythonhelpers.dataclass_annotate import DataclassAnnotateMixin

from ledboardlib import ControlParameters


@dataclass
class UiControlParameters(ControlParameters, DataclassAnnotateMixin):
    noise_octaves: IntegerSliderType("Noise octaves", (0, 4)) = 0
    noise_scale: IntegerSliderType("Noise scale", (0, 8)) = 1

    noise_scale_x: IntegerSliderType("Noise scale X", (0, 200)) = 20
    noise_scale_y: IntegerSliderType("Noise scale Y", (0, 200)) = 20

    noise_speed_x: IntegerSliderType("Noise speed X", (0, 100)) = 0
    noise_speed_y: IntegerSliderType("Noise speed Y", (0, 100)) = 0
    noise_speed_z: IntegerSliderType("Noise speed Z", (0, 100)) = 0

    noise_min: IntegerSliderType("Noise min", (0, 255)) = 0
    noise_max: IntegerSliderType("Noise max", (0, 255)) = 255

    noise_r: IntegerSliderType("Noise R", (0, 255)) = 0
    noise_g: IntegerSliderType("Noise G", (0, 255)) = 200
    noise_b: IntegerSliderType("Noise B", (0, 255)) = 200

    runner_r: IntegerSliderType("Runner R", (0, 255)) = 255
    runner_g: IntegerSliderType("Runner G", (0, 255)) = 0
    runner_b: IntegerSliderType("Runner B", (0, 255)) = 0

    runner_trigger: ButtonType("Runner trigger", (0, 1)) = 0
    are_colors_inverted: CheckBoxType("Are colors inverted?", (0, 1)) = 0
    is_noise_on: CheckBoxType("Is noise on?", (0, 1)) = 1

    # > 0: additive, < 0: multiply
    mask_x1: IntegerSliderType("Mask X1", (-255, 255)) = 0
    mask_x2: IntegerSliderType("Mask X2", (-255, 255)) = 0
    mask_y1: IntegerSliderType("Mask Y1", (-255, 255)) = 0
    mask_y2: IntegerSliderType("Mask Y2", (-255, 255)) = 0

    bat_low: CheckBoxType("Bat low", (0, 1)) = 0
    bat_1_bar: CheckBoxType("Bat 1 bar", (0, 1)) = 0

    @staticmethod
    def from_base(base: ControlParameters | None = None):  # FIXME None used for dev purposes
        return UiControlParameters()
