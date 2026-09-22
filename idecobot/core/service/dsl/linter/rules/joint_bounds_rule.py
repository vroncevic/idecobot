# -*- coding: UTF-8 -*-

'''
Module
    joint_bounds_rule.py
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
    Defines JointBoundsRule validating joint angles against mechanical limits.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import MyCobotDiagnosticSeverity
from idecobot.core.service.kinematics.ikinematic_validator import IKinematicValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointBoundsRule:
    '''
        Validates that all specified joint angles fall within robot safety boundaries.

        It defines:

            :attributes:
                | RULE_NAME - Unique identifier string for this rule ('joint_bounds').
                | DIAGNOSTIC_CODE - Diagnostic error code ('ERR_JOINT_BOUNDS').
                | _validator - IKinematicValidator domain service.
            :methods:
                | __init__ - Initializes rule with kinematic validator.
                | lint - Checks all joint movement instructions in program.
                | get_name - Returns rule identifier name.
                | get_version - Returns rule version string.
    '''

    RULE_NAME: ClassVar[str] = 'joint_bounds'
    DIAGNOSTIC_CODE: ClassVar[str] = 'ERR_JOINT_BOUNDS'

    _validator: IKinematicValidator

    def __init__(self, validator: IKinematicValidator) -> None:
        '''
            Initializes JointBoundsRule with kinematic validator.

            :param validator: Injected IKinematicValidator instance.
            :exceptions: None.
        '''
        self._validator = validator

    def get_name(self) -> str:
        '''
            Returns rule identifier name.

            :return: String identifier of this rule.
            :exceptions: None.
        '''
        return self.RULE_NAME

    def lint(self, program: MyCobotProgram) -> Sequence[MyCobotDiagnostic]:
        '''
            Analyzes program for joint angles that exceed mechanical limits.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of joint limit violation diagnostics.
            :exceptions: None.
        '''
        diagnostics: list[MyCobotDiagnostic] = []

        for inst in program.instructions:
            if inst.command_type != MyCobotCommandType.MOVE_JOINTS:
                continue

            for joint_id in range(1, 7):
                key: str = f'j{joint_id}'

                if key in inst.parameters:
                    val: float = inst.parameters[key]

                    if not self._validator.is_joint_in_range(joint_id, val):
                        diagnostics.append(
                            MyCobotDiagnostic(
                                line_number=inst.line_number,
                                severity=MyCobotDiagnosticSeverity.ERROR,
                                code=self.DIAGNOSTIC_CODE,
                                message=(
                                    f'Joint J{joint_id} angle {val:.2f}° exceeds '
                                    f'safe mechanical range.'
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

