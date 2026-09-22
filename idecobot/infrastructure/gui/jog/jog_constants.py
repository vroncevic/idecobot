# -*- coding: UTF-8 -*-

'''
Module
    jog_constants.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    idecobot is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    idecobot is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines JogConstants dataclass encapsulating operational parameters for manual jog view.
'''

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class JogConstants:
    '''
        Immutable operational configuration, layout, presets, and defaults for manual jog view.

        It defines:

            :attributes:
                | frame_padx - Horizontal padding of individual jog subpanel frames.
                | frame_pady - Vertical padding of individual jog subpanel frames.
                | outer_padx - Outer container horizontal padding.
                | outer_pady - Outer container vertical padding.
                | label_width - Character width of axis descriptor labels (e.g., J1:, X:).
                | val_width - Character width of coordinate and angle value labels.
                | step_btn_width - Character width of jog increment/decrement buttons.
                | tool_btn_width - Character width of tool action buttons.
                | combo_width - Character width of step and speed comboboxes.
                | row_pady - Vertical padding between jog rows.
                | step_presets - Sequence of selectable step delta strings in degrees or mm.
                | speed_presets - Sequence of selectable speed percentage strings.
                | default_step_str - Baseline step increment string.
                | default_speed_str - Baseline operating speed percentage string.
                | default_step - Baseline step increment numerical value.
                | default_speed - Baseline operating speed percentage numerical value.
                | title_jog_config - Header label for jog configuration.
                | title_joint_jog - Header label for joint jog panel.
                | title_cart_jog - Header label for Cartesian jog panel.
                | title_tool_control - Header label for tool & servo panel.
                | label_step - Label text for step size selection.
                | label_speed - Label text for operating speed selection.
                | label_gripper - Label text for gripper control section.
                | label_servo_state - Label text for servo state control section.
                | btn_minus_text - Text for minus decrement button.
                | btn_plus_text - Text for plus increment button.
                | btn_grip_text - Text for grip button.
                | btn_release_text - Text for release button.
                | btn_power_on_text - Text for power on button.
                | btn_relax_text - Text for relax button.
                | btn_home_text - Text for zero home button.
                | text_gripper_idle - Default idle gripper state text.
                | unit_deg - Degree unit symbol.
                | unit_mm - Millimeter unit symbol.
                | default_angles - Tracked baseline joint angles in degrees (J1 to J6).
                | default_coords - Tracked baseline Cartesian coordinates [x, y, z, rx, ry, rz].
                | axis_map - Mapping of Cartesian axis symbols to coordinate array indices.
                | state_gripped - Tool gripper gripped status text.
                | state_released - Tool gripper released status text.
                | action_grip - Action verb for tool grip operation.
                | action_release - Action verb for tool release operation.
                | grip_action_grip - Integer action code for gripper close.
                | grip_action_release - Integer action code for gripper open.
                | action_power_on - Action verb for servo power on operation.
                | action_relax - Action verb for servo relax operation.
                | round_precision - Decimal precision for display and delta values.
                | linear_axes - Set of linear Cartesian axis symbols for reach boundary checks.
    '''

    frame_padx: int = 8
    frame_pady: int = 4
    outer_padx: int = 4
    outer_pady: int = 4
    label_width: int = 3
    val_width: int = 7
    step_btn_width: int = 2
    tool_btn_width: int = 8
    combo_width: int = 8
    row_pady: int = 1
    step_presets: tuple[str, ...] = ('1.0', '5.0', '10.0', '20.0', '45.0')
    speed_presets: tuple[str, ...] = ('10', '20', '30', '50', '80', '100')
    default_step_str: str = '5.0'
    default_speed_str: str = '30'
    default_step: float = 5.0
    default_speed: int = 30
    title_jog_config: str = 'Jog Config'
    title_joint_jog: str = 'Joint Jog (J1-J6)'
    title_cart_jog: str = 'Cartesian Jog (X-Rz)'
    title_tool_control: str = 'Tool & Servo'
    label_step: str = 'Step (deg/mm):'
    label_speed: str = 'Speed (%):'
    label_gripper: str = 'Gripper:'
    label_servo_state: str = 'Servo State:'
    btn_minus_text: str = '-'
    btn_plus_text: str = '+'
    btn_grip_text: str = 'Grip'
    btn_release_text: str = 'Release'
    btn_power_on_text: str = '⚡ Power On'
    btn_relax_text: str = '🔓 Relax'
    btn_home_text: str = '⌂ Zero Home'
    text_gripper_idle: str = 'State: Idle'
    unit_deg: str = '°'
    unit_mm: str = 'mm'
    default_angles: tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    default_coords: tuple[float, ...] = (0.0, 150.0, 200.0, 0.0, 0.0, 0.0)
    axis_map: MappingProxyType[str, int] = MappingProxyType(
        {'X': 0, 'Y': 1, 'Z': 2, 'Rx': 3, 'Ry': 4, 'Rz': 5}
    )
    state_gripped: str = 'Gripped'
    state_released: str = 'Released'
    action_grip: str = 'Grip'
    action_release: str = 'Release'
    grip_action_grip: int = 1
    grip_action_release: int = 0
    action_power_on: str = 'Power On'
    action_relax: str = 'Relax'
    round_precision: int = 2
    linear_axes: frozenset[str] = frozenset({'X', 'Y', 'Z'})
