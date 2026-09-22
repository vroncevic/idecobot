# -*- coding: UTF-8 -*-

'''
Module
    workspace_reach_rule.py
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
    Defines WorkspaceReachRule validating Cartesian reach against physical limits.
'''

from __future__ import annotations

from collections.abc import Sequence
from math import sqrt
from typing import ClassVar

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import MyCobotDiagnosticSeverity
from idecobot.core.model.kinematics.spatial_bounds import SpatialBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceReachRule:
    '''
        Validates Cartesian positions against the spherical reach limit of the arm.

        It defines:

            :attributes:
                | RULE_NAME - Unique identifier string for this rule ('workspace_reach').
                | DIAGNOSTIC_CODE - Diagnostic error code ('ERR_WORKSPACE_REACH').
                | _bounds - SpatialBounds domain limits.
            :methods:
                | __init__ - Initializes rule with kinematic bounds.
                | lint - Checks all cartesian movement instructions in program.
                | get_name - Returns rule identifier name.
                | get_version - Returns rule version string.
    '''

    RULE_NAME: ClassVar[str] = 'workspace_reach'
    DIAGNOSTIC_CODE: ClassVar[str] = 'ERR_WORKSPACE_REACH'

    _bounds: SpatialBounds

    def __init__(self, bounds: SpatialBounds) -> None:
        '''
            Initializes WorkspaceReachRule with spatial boundaries.

            :param bounds: Injected SpatialBounds instance.
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
            Analyzes program for cartesian targets exceeding maximum reach.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of reach violation diagnostics.
            :exceptions: None.
        '''
        diagnostics: list[MyCobotDiagnostic] = []

        for inst in program.instructions:
            if inst.command_type != MyCobotCommandType.MOVE_COORDS:
                continue

            x: float = inst.parameters.get('x', 0.0)
            y: float = inst.parameters.get('y', 0.0)
            z: float = inst.parameters.get('z', 0.0)
            dist: float = sqrt(x * x + y * y + z * z)

            if dist > self._bounds.max_reach_mm:
                diagnostics.append(
                    MyCobotDiagnostic(
                        line_number=inst.line_number,
                        severity=MyCobotDiagnosticSeverity.ERROR,
                        code=self.DIAGNOSTIC_CODE,
                        message=(
                            f'Cartesian target distance {dist:.1f} mm exceeds '
                            f'maximum arm reach {self._bounds.max_reach_mm:.1f} mm.'
                        )
                    )
                )

        return tuple(diagnostics)

    def get_version(self) -> str:
        '''
            Returns rule version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

