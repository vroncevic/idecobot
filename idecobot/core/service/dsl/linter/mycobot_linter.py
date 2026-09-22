# -*- coding: UTF-8 -*-

'''
Module
    mycobot_linter.py
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
    Defines concrete MyCobotLinter executing injected semantic AST rules.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import MyCobotDiagnosticSeverity
from idecobot.core.service.dsl.linter.rules.imycobot_lint_rule import IMyCobotLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotLinter:
    '''
        Evaluates myCobot AST programs against injected domain safety and kinematic rules.

        It defines:

            :attributes:
                | _rules - Tuple of configured IMyCobotLintRule instances.
            :methods:
                | __init__ - Initializes linter with injected rule abstractions.
                | lint - Executes rules and returns sorted diagnostics.
                | is_valid - Checks whether program contains any error-level diagnostics.
                | get_version - Returns linter version string.
    '''

    _rules: tuple[IMyCobotLintRule, ...]

    def __init__(self, rules: Sequence[IMyCobotLintRule]) -> None:
        '''
            Initializes linter with domain safety rules.

            :param rules: Sequence of IMyCobotLintRule implementations.
            :exceptions: None.
        '''
        self._rules = tuple(rules)

    def lint(self, program: MyCobotProgram) -> Sequence[MyCobotDiagnostic]:
        '''
            Evaluates AST program across configured semantic rules.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of all identified diagnostic findings sorted by line.
            :exceptions: None.
        '''
        diagnostics: list[MyCobotDiagnostic] = []

        for rule in self._rules:
            findings: Sequence[MyCobotDiagnostic] = rule.lint(program)
            diagnostics.extend(findings)

        diagnostics.sort(key=lambda item: item.line_number)

        return tuple(diagnostics)

    def is_valid(self, program: MyCobotProgram) -> bool:
        '''
            Checks whether program contains any error-level diagnostics.

            :param program: Parsed MyCobotProgram AST instance.
            :return: True if program has no errors, False otherwise.
            :exceptions: None.
        '''
        return not any(
            d.severity == MyCobotDiagnosticSeverity.ERROR for d in self.lint(program)
        )

    def get_version(self) -> str:
        '''
            Returns linter version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

