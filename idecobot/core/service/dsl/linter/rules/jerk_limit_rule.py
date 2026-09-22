# -*- coding: UTF-8 -*-

'''
Module
    jerk_limit_rule.py
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
    Defines JerkLimitRule warning on sudden large angular joint changes.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import MyCobotDiagnosticSeverity
from idecobot.core.model.kinematics.trajectory_bounds import TrajectoryBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JerkLimitRule:
    '''
        Emits warning diagnostics when angular change between steps exceeds threshold.

        It defines:

            :attributes:
                | RULE_NAME - Unique identifier string for this rule ('jerk_limit').
                | DIAGNOSTIC_CODE - Diagnostic warning code ('WARN_LARGE_JERK').
                | _bounds - TrajectoryBounds domain limits.
            :methods:
                | __init__ - Initializes rule with kinematic bounds.
                | lint - Checks consecutive joint movements for excessive angular delta.
                | get_name - Returns rule identifier name.
                | get_version - Returns rule version string.
    '''

    RULE_NAME: ClassVar[str] = 'jerk_limit'
    DIAGNOSTIC_CODE: ClassVar[str] = 'WARN_LARGE_JERK'

    _bounds: TrajectoryBounds

    def __init__(self, bounds: TrajectoryBounds) -> None:
        '''
            Initializes JerkLimitRule with trajectory boundaries.

            :param bounds: Injected TrajectoryBounds instance.
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
            Analyzes consecutive joint move instructions for large angular jumps.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of jerk warning diagnostics.
            :exceptions: None.
        '''
        diagnostics: list[MyCobotDiagnostic] = []
        last_joints: dict[str, float] = {}

        for inst in program.instructions:
            if inst.command_type == MyCobotCommandType.HOME:
                last_joints = {f'j{i}': 0.0 for i in range(1, 7)}
                continue

            if inst.command_type != MyCobotCommandType.MOVE_JOINTS:
                continue

            for joint_id in range(1, 7):
                key: str = f'j{joint_id}'

                if key in inst.parameters and key in last_joints:
                    delta: float = abs(inst.parameters[key] - last_joints[key])

                    if delta > self._bounds.max_jerk_deg:
                        diagnostics.append(
                            MyCobotDiagnostic(
                                line_number=inst.line_number,
                                severity=MyCobotDiagnosticSeverity.WARNING,
                                code=self.DIAGNOSTIC_CODE,
                                message=(
                                    f'Joint J{joint_id} angular delta {delta:.1f}° '
                                    f'exceeds smooth trajectory threshold '
                                    f'{self._bounds.max_jerk_deg:.1f}°.'
                                )
                            )
                        )

                if key in inst.parameters:
                    last_joints[key] = inst.parameters[key]

        return tuple(diagnostics)

    def get_version(self) -> str:
        '''
            Returns rule version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

