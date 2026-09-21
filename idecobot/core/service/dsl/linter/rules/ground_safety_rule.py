# -*- coding: UTF-8 -*-

'''
Module
    ground_safety_rule.py
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
    Defines GroundSafetyRule preventing vertical collision below mounting table.
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


class GroundSafetyRule:
    '''
        Validates that Cartesian Z coordinate does not penetrate below safety plane.

        It defines:

            :attributes:
                | RULE_NAME - Unique identifier string for this rule ('ground_safety').
                | DIAGNOSTIC_CODE - Diagnostic error code ('ERR_GROUND_COLLISION').
                | _bounds - MyCobotBounds domain limits.
            :methods:
                | __init__ - Initializes rule with kinematic bounds.
                | lint - Checks all cartesian movements for floor collision.
                | get_name - Returns rule identifier name.
    '''

    RULE_NAME: ClassVar[str] = 'ground_safety'
    DIAGNOSTIC_CODE: ClassVar[str] = 'ERR_GROUND_COLLISION'

    _bounds: MyCobotBounds

    def __init__(self, bounds: MyCobotBounds) -> None:
        '''
            Initializes GroundSafetyRule with kinematic boundaries.

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
            Analyzes program for vertical coordinates below safety ground plane.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of ground safety violation diagnostics.
            :exceptions: None.
        '''
        diagnostics: list[MyCobotDiagnostic] = []

        for inst in program.instructions:
            if inst.command_type != MyCobotCommandType.MOVE_COORDS:
                continue

            if 'z' in inst.parameters:
                z_val: float = inst.parameters['z']

                if z_val < self._bounds.min_z_mm:
                    diagnostics.append(
                        MyCobotDiagnostic(
                            line_number=inst.line_number,
                            severity=MyCobotDiagnosticSeverity.ERROR,
                            code=self.DIAGNOSTIC_CODE,
                            message=(
                                f'Z height {z_val:.1f} mm is below table safety '
                                f'threshold {self._bounds.min_z_mm:.1f} mm.'
                            )
                        )
                    )

        return tuple(diagnostics)
