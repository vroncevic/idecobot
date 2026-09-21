# -*- coding: UTF-8 -*-

'''
Module
    mycobot_diagnostic.py
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
    Defines MyCobotDiagnostic immutable finding report model.
'''

from __future__ import annotations

from dataclasses import dataclass

from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import (
    MyCobotDiagnosticSeverity,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MyCobotDiagnostic:
    '''
        Represents a semantic analysis or linting finding on DSL source code.

        It defines:

            :attributes:
                | line_number - Source line number associated with diagnostic.
                | severity - Diagnostic severity (INFO, WARNING, ERROR).
                | code - Short machine-readable violation code.
                | message - Human-readable explanation of the issue.
            :methods:
                | format_report - Returns formatted diagnostic string.
                | is_error - Verifies if diagnostic has ERROR severity.
                | to_dict - Serializes diagnostic to dictionary representation.
    '''

    line_number: int
    severity: MyCobotDiagnosticSeverity
    code: str
    message: str

    def format_report(self) -> str:
        '''
            Returns formatted diagnostic representation.

            :return: Formatted report line string.
            :exceptions: None.
        '''
        return f'[{self.severity.value}] Line {self.line_number}: ({self.code}) {self.message}'

    def is_error(self) -> bool:
        '''
            Verifies if diagnostic is an ERROR severity violation.

            :return: True if severity is ERROR, False otherwise.
            :exceptions: None.
        '''
        return self.severity == MyCobotDiagnosticSeverity.ERROR

    def to_dict(self) -> dict[str, object]:
        '''
            Serializes diagnostic to dictionary representation.

            :return: Dictionary representation of diagnostic.
            :exceptions: None.
        '''
        return {
            'line_number': self.line_number,
            'severity': self.severity.value,
            'code': self.code,
            'message': self.message,
        }
