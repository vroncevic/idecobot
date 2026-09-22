# -*- coding: UTF-8 -*-

'''
Module
    compiler_test.py
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
    Unit tests for modular DSL command compilers and compilation context.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.service.dsl.compiler.commands.home_command_compiler import (
    HomeCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.icommand_compiler import (
    ICommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.move_coords_command_compiler import (
    MoveCoordsCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.move_joints_command_compiler import (
    MoveJointsCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.power_command_compiler import (
    PowerCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.relax_command_compiler import (
    RelaxCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.speed_command_compiler import (
    SpeedCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.tool_command_compiler import (
    ToolCommandCompiler,
)
from idecobot.core.service.dsl.compiler.commands.wait_command_compiler import (
    WaitCommandCompiler,
)
from idecobot.core.service.dsl.compiler.compiler_context import CompilerContext
from idecobot.core.service.dsl.compiler.imycobot_compiler import IMyCobotCompiler
from idecobot.core.service.dsl.compiler.mycobot_compiler import MyCobotCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompilerComponents(TestCase):
    '''
        Unit tests for individual command compilers, CompilerContext, and MyCobotCompiler.

        It defines:

            :methods:
                | setUp - Initializes fixtures with protocol constants and context.
                | test_protocols - Tests structural subtyping of compiler protocols.
                | test_home_compiler - Tests HomeCommandCompiler frame emission.
                | test_move_joints_compiler - Tests MoveJointsCommandCompiler.
                | test_move_coords_compiler - Tests MoveCoordsCommandCompiler.
                | test_tool_compiler - Tests ToolCommandCompiler grip and release.
                | test_power_and_relax_compilers - Tests Power and Relax compilers.
                | test_speed_and_wait_compilers - Tests Speed and Wait compilers.
                | test_compiler_context - Tests CompilerContext state operations.
                | test_mycobot_compiler - Tests MyCobotCompiler program coordination.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures for compiler tests.
        '''
        self.constants = ProtocolConstants()
        self.default_speed = 30
        self.default_delay = self.constants.default_frame_delay

    def test_protocols(self) -> None:
        '''
            Tests structural subtyping of ICommandCompiler and IMyCobotCompiler.
        '''
        home = HomeCommandCompiler(constants=self.constants)
        self.assertIsInstance(home, ICommandCompiler)
        self.assertTrue(len(home.get_version()) > 0)

        compiler = MyCobotCompiler(compilers=[home], default_speed=self.default_speed)
        self.assertIsInstance(compiler, IMyCobotCompiler)
        self.assertTrue(len(compiler.get_version()) > 0)

    def test_home_compiler(self) -> None:
        '''
            Tests HomeCommandCompiler emits valid frame and resets angles.
        '''
        compiler = HomeCommandCompiler(constants=self.constants)
        context = CompilerContext(default_speed=self.default_speed)
        context.angles[0] = 45.0

        self.assertTrue(compiler.can_compile(MyCobotCommandType.HOME))
        self.assertFalse(compiler.can_compile(MyCobotCommandType.MOVE_JOINTS))

        inst = MyCobotInstruction(
            command_type=MyCobotCommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='HOME'
        )
        frames = compiler.compile(inst, context)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].cmd_id, self.constants.cmd_send_angles)
        self.assertEqual(context.angles, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    def test_move_joints_compiler(self) -> None:
        '''
            Tests MoveJointsCommandCompiler updates angles and emits SEND_ANGLES frame.
        '''
        compiler = MoveJointsCommandCompiler(
            constants=self.constants, default_delay=self.default_delay
        )
        context = CompilerContext(default_speed=self.default_speed)

        self.assertTrue(compiler.can_compile(MyCobotCommandType.MOVE_JOINTS))
        self.assertFalse(compiler.can_compile(MyCobotCommandType.HOME))

        inst = MyCobotInstruction(
            command_type=MyCobotCommandType.MOVE_JOINTS,
            parameters={'j1': 10.0, 'j2': -20.0, 'speed': 50},
            line_number=1,
            raw_text='MOVE J1:10 J2:-20 SPEED:50'
        )
        frames = compiler.compile(inst, context)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].cmd_id, self.constants.cmd_send_angles)
        self.assertEqual(context.angles[0], 10.0)
        self.assertEqual(context.angles[1], -20.0)

    def test_move_coords_compiler(self) -> None:
        '''
            Tests MoveCoordsCommandCompiler updates coordinates and emits SEND_COORDS frame.
        '''
        compiler = MoveCoordsCommandCompiler(
            constants=self.constants, default_delay=self.default_delay
        )
        context = CompilerContext(default_speed=self.default_speed)

        self.assertTrue(compiler.can_compile(MyCobotCommandType.MOVE_COORDS))
        self.assertFalse(compiler.can_compile(MyCobotCommandType.MOVE_JOINTS))

        inst = MyCobotInstruction(
            command_type=MyCobotCommandType.MOVE_COORDS,
            parameters={'x': 100.0, 'z': 250.0, 'speed': 40, 'mode': 1},
            line_number=1,
            raw_text='MOVE X:100 Z:250 SPEED:40'
        )
        frames = compiler.compile(inst, context)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].cmd_id, self.constants.cmd_send_coords)
        self.assertEqual(context.coords[0], 100.0)
        self.assertEqual(context.coords[2], 250.0)

    def test_tool_compiler(self) -> None:
        '''
            Tests ToolCommandCompiler encodes grip and release states.
        '''
        compiler = ToolCommandCompiler(constants=self.constants)
        context = CompilerContext(default_speed=self.default_speed)

        self.assertTrue(compiler.can_compile(MyCobotCommandType.TOOL))
        self.assertFalse(compiler.can_compile(MyCobotCommandType.POWER))

        inst_grip = MyCobotInstruction(
            command_type=MyCobotCommandType.TOOL,
            parameters={'action': 'GRIP', 'speed': 80},
            line_number=1,
            raw_text='TOOL GRIP SPEED:80'
        )
        frames = compiler.compile(inst_grip, context)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].cmd_id, self.constants.cmd_set_gripper)

        inst_release = MyCobotInstruction(
            command_type=MyCobotCommandType.TOOL,
            parameters={'action': 'RELEASE'},
            line_number=2,
            raw_text='TOOL RELEASE'
        )
        frames = compiler.compile(inst_release, context)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].cmd_id, self.constants.cmd_set_gripper)

    def test_power_and_relax_compilers(self) -> None:
        '''
            Tests PowerCommandCompiler and RelaxCommandCompiler frames.
        '''
        power = PowerCommandCompiler(constants=self.constants)
        relax = RelaxCommandCompiler(constants=self.constants)
        context = CompilerContext(default_speed=self.default_speed)

        self.assertTrue(power.can_compile(MyCobotCommandType.POWER))
        self.assertTrue(relax.can_compile(MyCobotCommandType.RELAX))

        inst_p = MyCobotInstruction(
            command_type=MyCobotCommandType.POWER,
            parameters={},
            line_number=1,
            raw_text='POWER'
        )
        frames_p = power.compile(inst_p, context)
        self.assertEqual(len(frames_p), 1)
        self.assertEqual(frames_p[0].cmd_id, self.constants.cmd_power_on)

        inst_r = MyCobotInstruction(
            command_type=MyCobotCommandType.RELAX,
            parameters={},
            line_number=2,
            raw_text='RELAX'
        )
        frames_r = relax.compile(inst_r, context)
        self.assertEqual(len(frames_r), 1)
        self.assertEqual(frames_r[0].cmd_id, self.constants.cmd_release_servos)

    def test_speed_and_wait_compilers(self) -> None:
        '''
            Tests SpeedCommandCompiler and WaitCommandCompiler operations.
        '''
        speed = SpeedCommandCompiler(default_speed=self.default_speed)
        wait = WaitCommandCompiler(constants=self.constants)
        context = CompilerContext(default_speed=self.default_speed)

        self.assertTrue(speed.can_compile(MyCobotCommandType.SPEED))
        self.assertTrue(wait.can_compile(MyCobotCommandType.WAIT))

        inst_s = MyCobotInstruction(
            command_type=MyCobotCommandType.SPEED,
            parameters={'value': 75},
            line_number=1,
            raw_text='SPEED 75'
        )
        frames_s = speed.compile(inst_s, context)
        self.assertEqual(len(frames_s), 0)
        self.assertEqual(context.speed, 75)

        # WAIT without preceding frames produces NOP frame
        inst_w = MyCobotInstruction(
            command_type=MyCobotCommandType.WAIT,
            parameters={'seconds': 1.5},
            line_number=2,
            raw_text='WAIT 1.5'
        )
        frames_w = wait.compile(inst_w, context)
        self.assertEqual(len(frames_w), 1)
        self.assertEqual(frames_w[0].cmd_id, self.constants.cmd_nop)
        self.assertEqual(frames_w[0].delay_after_sec, 1.5)

        # WAIT with preceding frame extends delay
        context.add_frame(MyCobotFrame(self.constants.cmd_power_on, b'', 0.2))
        frames_w2 = wait.compile(inst_w, context)
        self.assertEqual(len(frames_w2), 0)
        self.assertAlmostEqual(context.frames[-1].delay_after_sec, 1.7)

    def test_compiler_context(self) -> None:
        '''
            Tests CompilerContext state methods.
        '''
        context = CompilerContext(default_speed=30)
        self.assertEqual(context.speed, 30)
        self.assertTrue(len(context.get_version()) > 0)

        context.angles[0] = 10.0
        context.reset_angles()
        self.assertEqual(context.angles[0], 0.0)

        self.assertFalse(context.add_delay_to_last_frame(0.5))
        context.add_frame(MyCobotFrame(0x01, b'', 0.1))
        self.assertTrue(context.add_delay_to_last_frame(0.5))
        self.assertAlmostEqual(context.frames[-1].delay_after_sec, 0.6)

    def test_mycobot_compiler(self) -> None:
        '''
            Tests MyCobotCompiler program coordination and single instruction compile.
        '''
        compilers = [
            HomeCommandCompiler(constants=self.constants),
            RelaxCommandCompiler(constants=self.constants),
            PowerCommandCompiler(constants=self.constants),
            SpeedCommandCompiler(default_speed=self.default_speed),
            WaitCommandCompiler(constants=self.constants),
            ToolCommandCompiler(constants=self.constants),
            MoveJointsCommandCompiler(
                constants=self.constants, default_delay=self.default_delay
            ),
            MoveCoordsCommandCompiler(
                constants=self.constants, default_delay=self.default_delay
            )
        ]
        compiler = MyCobotCompiler(compilers=compilers, default_speed=self.default_speed)
        inst = MyCobotInstruction(
            command_type=MyCobotCommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='HOME'
        )
        single_frames = compiler.compile_instruction(inst)
        self.assertEqual(len(single_frames), 1)

        program = MyCobotProgram(instructions=(inst,))
        prog_frames = compiler.compile(program)
        self.assertEqual(len(prog_frames), 1)


if __name__ == '__main__':
    main()
