# -*- coding: UTF-8 -*-

'''
Module
    test_dsl.py
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
    Unit tests for DSL Lexer, Parser, Linter, Compiler, and Facade Service.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.model.kinematics.joint_bounds import JointBounds
from idecobot.core.model.kinematics.joint_limit import JointLimit
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.model.kinematics.spatial_bounds import SpatialBounds
from idecobot.core.model.kinematics.speed_bounds import SpeedBounds
from idecobot.core.model.kinematics.trajectory_bounds import TrajectoryBounds
from idecobot.core.service.kinematics.kinematic_validator import KinematicValidator
from idecobot.core.service.dsl.compiler.commands.home_command_compiler import (
    HomeCommandCompiler,
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
from idecobot.core.service.dsl.compiler.mycobot_compiler import MyCobotCompiler
from idecobot.core.service.dsl.lexer.mycobot_lexer import MyCobotLexer
from idecobot.core.service.dsl.linter.mycobot_linter import MyCobotLinter
from idecobot.core.service.dsl.linter.rules.ground_safety_rule import GroundSafetyRule
from idecobot.core.service.dsl.linter.rules.jerk_limit_rule import JerkLimitRule
from idecobot.core.service.dsl.linter.rules.joint_bounds_rule import JointBoundsRule
from idecobot.core.service.dsl.linter.rules.speed_limit_rule import SpeedLimitRule
from idecobot.core.service.dsl.linter.rules.workspace_reach_rule import WorkspaceReachRule
from idecobot.core.service.dsl.mycobot_dsl_service import MyCobotDslService
from idecobot.core.service.dsl.parser.commands.home_command_parser import HomeCommandParser
from idecobot.core.service.dsl.parser.commands.move_command_parser import MoveCommandParser
from idecobot.core.service.dsl.parser.commands.power_command_parser import PowerCommandParser
from idecobot.core.service.dsl.parser.commands.relax_command_parser import RelaxCommandParser
from idecobot.core.service.dsl.parser.commands.speed_command_parser import SpeedCommandParser
from idecobot.core.service.dsl.parser.commands.tool_command_parser import ToolCommandParser
from idecobot.core.service.dsl.parser.commands.wait_command_parser import WaitCommandParser
from idecobot.core.service.dsl.parser.mycobot_parser import MyCobotParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotDsl(TestCase):
    '''
        Test cases for full DSL lexing, parsing, semantic linting, and compiling pipeline.

        It defines:

            :methods:
                | test_lexer_tokenization - Tests token stream generation.
                | test_parser_instructions - Tests parsing commands into AST.
                | test_linter_bounds_error - Tests detection of joint limit violation.
                | test_compiler_bytecode - Tests binary frame compilation.
                | test_dsl_service_pipeline - Tests high-level DSL service facade.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with full DSL service.
        '''
        bounds = MyCobotBounds(
            joints=JointBounds(
                j1=JointLimit(min_deg=-165.0, max_deg=165.0),
                j2=JointLimit(min_deg=-165.0, max_deg=165.0),
                j3=JointLimit(min_deg=-165.0, max_deg=165.0),
                j4=JointLimit(min_deg=-165.0, max_deg=165.0),
                j5=JointLimit(min_deg=-165.0, max_deg=165.0),
                j6=JointLimit(min_deg=-175.0, max_deg=175.0)
            ),
            spatial=SpatialBounds(max_reach_mm=285.0, min_z_mm=-10.0),
            speed=SpeedBounds(min_speed=1, max_speed=100, default_speed=30),
            trajectory=TrajectoryBounds(max_jerk_deg=60.0)
        )
        validator = KinematicValidator(bounds=bounds)
        grammar = DslGrammarConstants()
        self.lexer = MyCobotLexer(grammar=grammar)
        self.parser = MyCobotParser(parsers=[
            HomeCommandParser(),
            RelaxCommandParser(),
            PowerCommandParser(),
            SpeedCommandParser(),
            WaitCommandParser(),
            ToolCommandParser(grammar=grammar),
            MoveCommandParser(grammar=grammar)
        ])
        self.linter = MyCobotLinter(rules=[
            JointBoundsRule(validator=validator),
            WorkspaceReachRule(bounds=bounds.spatial),
            GroundSafetyRule(bounds=bounds.spatial),
            JerkLimitRule(bounds=bounds.trajectory),
            SpeedLimitRule(bounds=bounds.speed)
        ])
        protocol_constants = ProtocolConstants()
        self.compiler = MyCobotCompiler(
            compilers=[
                HomeCommandCompiler(constants=protocol_constants),
                RelaxCommandCompiler(constants=protocol_constants),
                PowerCommandCompiler(constants=protocol_constants),
                SpeedCommandCompiler(default_speed=bounds.speed.default_speed),
                WaitCommandCompiler(constants=protocol_constants),
                ToolCommandCompiler(constants=protocol_constants),
                MoveJointsCommandCompiler(
                    constants=protocol_constants,
                    default_delay=protocol_constants.default_frame_delay
                ),
                MoveCoordsCommandCompiler(
                    constants=protocol_constants,
                    default_delay=protocol_constants.default_frame_delay
                )
            ],
            default_speed=bounds.speed.default_speed
        )
        self.service = MyCobotDslService(
            lexer=self.lexer,
            parser=self.parser,
            linter=self.linter,
            compiler=self.compiler
        )

    def test_lexer_tokenization(self) -> None:
        '''
            Tests token stream generation from DSL source lines.
        '''
        source = 'MOVE J1:10 J2:20 SPEED:30'
        tokens = list(self.lexer.tokenize(source))
        self.assertGreaterEqual(len(tokens), 4)

    def test_parser_instructions(self) -> None:
        '''
            Tests parsing source code into valid MyCobotProgram.
        '''
        script = 'HOME\nSPEED 40\nWAIT 1.0\nTOOL GRIP'
        tokens = list(self.lexer.tokenize(script))
        program = self.parser.parse(tokens, script.splitlines())
        self.assertEqual(len(program.instructions), 4)

    def test_linter_bounds_error(self) -> None:
        '''
            Tests that linter flags out-of-bounds joint angles.
        '''
        script = 'MOVE J1:200 J2:0 J3:0'
        tokens = list(self.lexer.tokenize(script))
        program = self.parser.parse(tokens)
        diagnostics = list(self.linter.lint(program))
        self.assertTrue(any(d.severity.value == 'ERROR' for d in diagnostics))

    def test_compiler_bytecode(self) -> None:
        '''
            Tests compiling valid program into binary frames.
        '''
        script = 'HOME\nTOOL RELEASE\nRELAX'
        tokens = list(self.lexer.tokenize(script))
        program = self.parser.parse(tokens)
        frames = self.compiler.compile(program)
        self.assertEqual(len(frames), 3)

    def test_dsl_service_pipeline(self) -> None:
        '''
            Tests end-to-end validate and compile through DslService.
        '''
        script = 'HOME\nMOVE J1:10 J2:15 SPEED:30\nWAIT 0.5'
        prog, diags = self.service.validate(script)
        self.assertEqual(len(diags), 0)
        self.assertIsNotNone(prog)
        if prog:
            frames = self.service.compile(prog)
            self.assertEqual(len(frames), 2)


if __name__ == '__main__':
    main()
