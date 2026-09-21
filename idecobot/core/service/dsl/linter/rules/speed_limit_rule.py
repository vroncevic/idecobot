# -*- coding: UTF-8 -*-

'''
Module
    speed_limit_rule.py
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
    Defines SpeedLimitRule validating speed percentages.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import (
    MyCobotDiagnosticSeverity,
)
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpeedLimitRule:
    '''
        Validates that speed parameters remain within allowable percentage bounds.

        It defines:

            :attributes:
                | RULE_NAME - Unique identifier string for this rule ('speed_limit').
                | DIAGNOSTIC_CODE - Diagnostic error code ('ERR_SPEED_BOUNDS').
                | _bounds - MyCobotBounds domain limits.
            :methods:
                | __init__ - Initializes rule with kinematic bounds.
                | lint - Checks all speed values in program instructions.
                | get_name - Returns rule identifier name.
    '''

    RULE_NAME: ClassVar[str] = 'speed_limit'
    DIAGNOSTIC_CODE: ClassVar[str] = 'ERR_SPEED_BOUNDS'

    _bounds: MyCobotBounds

    def __init__(self, bounds: MyCobotBounds) -> None:
        '''
            Initializes SpeedLimitRule with kinematic boundaries.

            :param bounds: Injected MyCobotBounds instance.
            :exceptions: None.
        '''
        self._bounds = bounds

    def get_name(self) -> str:
        '''
            Returns rule identifier name.

            :return: String identifier of this rule.
            :exceptions: None.
        '''
        return self.RULE_NAME

    def lint(self, program: MyCobotProgram) -> Sequence[MyCobotDiagnostic]:
        '''
            Analyzes program instructions for speed values outside permitted range.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of speed violation diagnostics.
            :exceptions: None.
        '''
        diagnostics: list[MyCobotDiagnostic] = []

        for inst in program.instructions:
            speed_val: float | None = None

            if inst.command_type == MyCobotCommandType.SPEED:
                speed_val = inst.parameters.get('value')
            elif 'speed' in inst.parameters:
                speed_val = inst.parameters['speed']

            if speed_val is not None:
                if not (self._bounds.min_speed <= speed_val <= self._bounds.max_speed):
                    diagnostics.append(
                        MyCobotDiagnostic(
                            line_number=inst.line_number,
                            severity=MyCobotDiagnosticSeverity.ERROR,
                            code=self.DIAGNOSTIC_CODE,
                            message=(
                                f'Speed {speed_val}% is outside allowable '
                                f'[{self._bounds.min_speed}, {self._bounds.max_speed}]% range.'
                            )
                        )
                    )

        return tuple(diagnostics)
