# -*- coding: UTF-8 -*-

'''
Module
    mycobot_compiler.py
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
    Defines concrete MyCobotCompiler translating AST into binary frames.
'''

from __future__ import annotations

from collections.abc import Sequence
from struct import pack
from typing import ClassVar

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotCompiler:
    '''
        Translates parsed AST instructions into binary protocol frames.

        It defines:

            :attributes:
                | ACTION_GRIP - Action verb token for gripping ('GRIP').
                | ACTION_RELEASE - Action verb token for releasing ('RELEASE').
                | COORD_KEYS - Ordered tuple of Cartesian coordinate parameter names.
                | _constants - Injected ProtocolConstants protocol parameters.
                | _default_speed - Baseline velocity percentage.
                | _default_delay - Baseline delay after each move in seconds.
            :methods:
                | compile - Compiles entire MyCobotProgram into frames.
                | compile_instruction - Compiles a single AST instruction into serial frames.
                | _compile_move_joints - Compiles MOVE_JOINTS instruction.
                | _compile_move_coords - Compiles MOVE_COORDS instruction.
                | _compile_tool - Compiles TOOL gripper instruction.
    '''

    ACTION_GRIP: ClassVar[str] = 'GRIP'
    ACTION_RELEASE: ClassVar[str] = 'RELEASE'
    COORD_KEYS: ClassVar[tuple[str, ...]] = ('x', 'y', 'z', 'rx', 'ry', 'rz')

    _constants: ProtocolConstants
    _default_speed: int
    _default_delay: float

    def __init__(
        self,
        constants: ProtocolConstants,
        default_speed: int
    ) -> None:
        '''
            Initializes compiler with injected constants and motion parameters.

            :param constants: Injected ProtocolConstants instance.
            :param default_speed: Baseline velocity percentage (1-100).
            :exceptions: None.
        '''
        self._constants = constants
        self._default_speed = default_speed
        self._default_delay = constants.default_frame_delay

    def _compile_move_joints(
        self,
        inst: MyCobotInstruction,
        current_angles: list[float],
        speed: int
    ) -> MyCobotFrame:
        '''
            Translates joint move into SEND_ANGLES binary frame.

            :param inst: MOVE_JOINTS instruction.
            :param current_angles: Tracked list of 6 joint angles in degrees.
            :param speed: Operating velocity percentage.
            :return: MyCobotFrame instance.
            :exceptions: None.
        '''
        for idx in range(6):
            key: str = f'j{idx + 1}'

            if key in inst.parameters:
                current_angles[idx] = inst.parameters[key]

        scaled: list[int] = [
            int(round(ang * self._constants.angle_scale_factor))
            for ang in current_angles
        ]
        move_speed: int = int(inst.parameters.get('speed', speed))
        payload: bytes = pack(
            self._constants.format_angles_command,
            scaled[0], scaled[1], scaled[2],
            scaled[3], scaled[4], scaled[5],
            move_speed & self._constants.byte_mask
        )

        return MyCobotFrame(
            self._constants.cmd_send_angles,
            payload,
            self._default_delay
        )

    def _compile_move_coords(
        self,
        inst: MyCobotInstruction,
        current_coords: list[float],
        speed: int
    ) -> MyCobotFrame:
        '''
            Translates cartesian move into SEND_COORDS binary frame.

            :param inst: MOVE_COORDS instruction.
            :param current_coords: Tracked list of [x, y, z, rx, ry, rz].
            :param speed: Operating velocity percentage.
            :return: MyCobotFrame instance.
            :exceptions: None.
        '''
        for idx, key in enumerate(self.COORD_KEYS):
            if key in inst.parameters:
                current_coords[idx] = inst.parameters[key]

        scaled: list[int] = [
            int(round(val * self._constants.coord_scale_factor))
            for val in current_coords
        ]
        move_speed: int = int(inst.parameters.get('speed', speed))
        mode: int = int(inst.parameters.get('mode', 0))
        payload: bytes = pack(
            self._constants.format_coords_command,
            scaled[0], scaled[1], scaled[2],
            scaled[3], scaled[4], scaled[5],
            move_speed & self._constants.byte_mask,
            mode & self._constants.byte_mask
        )

        return MyCobotFrame(
            self._constants.cmd_send_coords,
            payload,
            self._default_delay
        )

    def _compile_tool(
        self,
        inst: MyCobotInstruction,
        speed: int
    ) -> MyCobotFrame:
        '''
            Translates tool command into SET_GRIPPER binary frame.

            :param inst: TOOL instruction.
            :param speed: Default velocity percentage.
            :return: MyCobotFrame instance.
            :exceptions: None.
        '''
        action: str = str(inst.parameters.get('action', self.ACTION_RELEASE))
        state: int = 1 if action == self.ACTION_GRIP else 0
        tool_speed: int = int(inst.parameters.get('speed', speed))
        payload: bytes = pack(
            self._constants.format_gripper_command,
            state & self._constants.byte_mask,
            tool_speed & self._constants.byte_mask
        )

        return MyCobotFrame(
            self._constants.cmd_set_gripper,
            payload,
            self._constants.gripper_delay
        )

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        '''
            Translates MyCobotProgram AST into sequence of MyCobotFrames.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of compiled binary MyCobotFrame objects.
            :exceptions: None.
        '''
        frames: list[MyCobotFrame] = []
        speed: int = self._default_speed
        angles: list[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        coords: list[float] = [0.0, 150.0, 200.0, 0.0, 0.0, 0.0]

        for inst in program.instructions:
            match inst.command_type:
                case MyCobotCommandType.HOME:
                    angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    payload = pack(
                        self._constants.format_angles_command,
                        0, 0, 0, 0, 0, 0,
                        speed & self._constants.byte_mask
                    )
                    frames.append(MyCobotFrame(
                        self._constants.cmd_send_angles,
                        payload,
                        self._constants.home_delay
                    ))
                case MyCobotCommandType.RELAX:
                    frames.append(MyCobotFrame(
                        self._constants.cmd_release_servos,
                        b'',
                        self._constants.servo_delay
                    ))
                case MyCobotCommandType.POWER:
                    frames.append(MyCobotFrame(
                        self._constants.cmd_power_on,
                        b'',
                        self._constants.servo_delay
                    ))
                case MyCobotCommandType.SPEED:
                    speed = int(inst.parameters.get('value', self._default_speed))
                case MyCobotCommandType.WAIT:
                    wait_sec: float = float(inst.parameters.get('seconds', 0.0))

                    if frames:
                        last: MyCobotFrame = frames[-1]
                        frames[-1] = MyCobotFrame(
                            last.cmd_id,
                            last.payload,
                            last.delay_after_sec + wait_sec
                        )
                    else:
                        frames.append(MyCobotFrame(
                            self._constants.cmd_nop,
                            b'',
                            wait_sec
                        ))

                case MyCobotCommandType.TOOL:
                    frames.append(self._compile_tool(inst, speed))
                case MyCobotCommandType.MOVE_JOINTS:
                    frames.append(self._compile_move_joints(inst, angles, speed))
                case MyCobotCommandType.MOVE_COORDS:
                    frames.append(self._compile_move_coords(inst, coords, speed))

        return tuple(frames)

    def compile_instruction(self, instruction: MyCobotInstruction) -> Sequence[MyCobotFrame]:
        '''
            Compiles a single AST instruction into a sequence of binary frames.

            :param instruction: Single MyCobotInstruction node.
            :return: Sequence of compiled MyCobotFrame instances.
            :exceptions: None.
        '''
        return self.compile(MyCobotProgram(instructions=(instruction,)))
