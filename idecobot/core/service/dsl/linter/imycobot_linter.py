# -*- coding: UTF-8 -*-

'''
Module
    imycobot_linter.py
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
    Defines structural interface protocol for the myCobot AST linter.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotLinter(Protocol):
    '''
        Defines structural interface protocol for linting myCobot AST programs.

        It defines:

            :methods:
                | lint - Evaluates AST program across configured semantic rules.
                | is_valid - Checks whether program contains any error-level diagnostics.
                | get_version - Returns protocol version string.
    '''

    def lint(self, program: MyCobotProgram) -> Sequence[MyCobotDiagnostic]:
        '''
            Evaluates AST program across configured semantic rules.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of all identified diagnostic findings.
        '''

    def is_valid(self, program: MyCobotProgram) -> bool:
        '''
            Checks whether program contains any error-level diagnostics.

            :param program: Parsed MyCobotProgram AST instance.
            :return: True if program has no errors, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
        '''

