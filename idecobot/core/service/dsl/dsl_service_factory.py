# -*- coding: UTF-8 -*-

'''
Module
    dsl_service_factory.py
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
    Defines DslServiceFactory assembling lexer, parser, linter, and compiler into DSL service.
'''

from __future__ import annotations

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.service.dsl.compiler.commands.home_command_compiler import HomeCommandCompiler
from idecobot.core.service.dsl.compiler.commands.move_coords_command_compiler import MoveCoordsCommandCompiler
from idecobot.core.service.dsl.compiler.commands.move_joints_command_compiler import MoveJointsCommandCompiler
from idecobot.core.service.dsl.compiler.commands.power_command_compiler import PowerCommandCompiler
from idecobot.core.service.dsl.compiler.commands.relax_command_compiler import RelaxCommandCompiler
from idecobot.core.service.dsl.compiler.commands.speed_command_compiler import SpeedCommandCompiler
from idecobot.core.service.dsl.compiler.commands.tool_command_compiler import ToolCommandCompiler
from idecobot.core.service.dsl.compiler.commands.wait_command_compiler import WaitCommandCompiler
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
from idecobot.core.service.kinematics.ikinematic_validator import IKinematicValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslServiceFactory:
    '''
        Factory assembling the complete domain DSL compiler and analyzer service.

        It defines:

            :methods:
                | create - Instantiates and wires parsers, linter rules, compiler, and service.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        bounds: MyCobotBounds,
        validator: IKinematicValidator,
        protocol_constants: ProtocolConstants,
        grammar: DslGrammarConstants
    ) -> MyCobotDslService:
        '''
            Builds and wires the DSL compiler and analysis subsystem.

            :param bounds: Manipulator kinematic boundary limits.
            :param validator: Injected IKinematicValidator domain service.
            :param protocol_constants: Low-level byte framing constants.
            :param grammar: DSL syntax grammar specifications.
            :return: Fully configured MyCobotDslService.
            :exceptions: None.
        '''
        command_parsers = [
            HomeCommandParser(),
            RelaxCommandParser(),
            PowerCommandParser(),
            SpeedCommandParser(),
            WaitCommandParser(),
            ToolCommandParser(grammar=grammar),
            MoveCommandParser(grammar=grammar)
        ]
        lint_rules = [
            JointBoundsRule(validator=validator),
            WorkspaceReachRule(bounds=bounds.spatial),
            GroundSafetyRule(bounds=bounds.spatial),
            JerkLimitRule(bounds=bounds.trajectory),
            SpeedLimitRule(bounds=bounds.speed)
        ]
        command_compilers = [
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
        ]

        return MyCobotDslService(
            lexer=MyCobotLexer(grammar=grammar),
            parser=MyCobotParser(parsers=command_parsers),
            linter=MyCobotLinter(rules=lint_rules),
            compiler=MyCobotCompiler(
                compilers=command_compilers,
                default_speed=bounds.speed.default_speed
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: The factory version string.
            :exceptions: None.
        '''
        return __version__
