# -*- coding: UTF-8 -*-

'''
Module
    test_editor_coordinator.py
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
    Unit tests for EditorCoordinator and EditorConstants.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import (
    MyCobotDiagnostic,
)
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import (
    MyCobotDiagnosticSeverity,
)
from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.editor.editor_coordinator import (
    EditorCoordinator,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockDslService:
    '''
        Mock DSL service implementing structural subtyping for IMyCobotDslService.
    '''

    def __init__(self) -> None:
        self.should_fail_validation: bool = False
        self.diagnostics_to_return: list[MyCobotDiagnostic] = []
        self.frames_to_return: list[MyCobotFrame] = [
            MyCobotFrame(
                cmd_id=0x20,
                payload=bytes([0x01]),
                delay_after_sec=0.0
            )
        ]

    def tokenize(self, code: str):
        return ()

    def parse(self, tokens):
        return MyCobotProgram()

    def lint(self, program):
        return ()

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        return self.frames_to_return

    def validate(
        self,
        code: str
    ) -> tuple[MyCobotProgram | None, Sequence[MyCobotDiagnostic]]:
        if self.should_fail_validation:
            return None, self.diagnostics_to_return
        return MyCobotProgram(), self.diagnostics_to_return


class TestEditorCoordinator(TestCase):
    '''
        Test cases for EditorCoordinator validation, compilation, and templates.

        It defines:

            :methods:
                | test_template_catalog - Verifies template loading and catalog listing.
                | test_validate_code_success - Verifies successful code validation.
                | test_validate_code_failure - Verifies validation failure with diagnostics.
                | test_compile_code_success - Verifies bytecode generation on valid code.
                | test_compile_code_failure - Verifies compilation abortion on invalid code.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with coordinator and mock DSL service.
        '''
        self.mock_service = MockDslService()
        self.constants = EditorConstants()
        self.logs: list[str] = []
        self.emitted_bytecode: list[Sequence[MyCobotFrame]] = []
        self.coordinator = EditorCoordinator(
            dsl_service=self.mock_service,
            on_bytecode=self.emitted_bytecode.append,
            on_log=self.logs.append,
            constants=self.constants
        )

    def test_template_catalog(self) -> None:
        '''
            Tests listing available templates and loading a specific template.
        '''
        templates: Sequence[str] = self.coordinator.get_available_templates()
        self.assertIn('Pick and Place', templates)

        script: str = self.coordinator.load_template('Pick and Place')
        self.assertIn('MOVE', script)
        self.assertTrue(any('Pick and Place' in msg for msg in self.logs))

    def test_validate_code_success(self) -> None:
        '''
            Tests successful code validation with zero errors.
        '''
        is_valid, summary, diags = self.coordinator.validate_code('MOVE J1 10.0')
        self.assertTrue(is_valid)
        self.assertEqual(summary, self.constants.msg_validation_passed)
        self.assertTrue(any(self.constants.msg_log_validation_passed in msg for msg in self.logs))

    def test_validate_code_failure(self) -> None:
        '''
            Tests validation failure reporting diagnostics and error summaries.
        '''
        self.mock_service.should_fail_validation = True
        self.mock_service.diagnostics_to_return = [
            MyCobotDiagnostic(
                line_number=3,
                severity=MyCobotDiagnosticSeverity.ERROR,
                code='SYNTAX_ERR',
                message='Invalid command syntax'
            )
        ]

        is_valid, summary, diags = self.coordinator.validate_code('INVALID SYNTAX')
        self.assertFalse(is_valid)
        self.assertIn('SYNTAX_ERR', summary)
        self.assertIn('Line 3', summary)
        self.assertTrue(any('SYNTAX_ERR' in msg for msg in self.logs))

    def test_compile_code_success(self) -> None:
        '''
            Tests compilation of valid code produces bytecode frames.
        '''
        success, summary, frames = self.coordinator.compile_code('MOVE J1 10.0')
        self.assertTrue(success)
        self.assertIsNotNone(frames)
        self.assertEqual(len(self.emitted_bytecode), 1)
        self.assertEqual(len(self.emitted_bytecode[0]), 1)
        self.assertTrue(any('Successfully compiled 1' in msg for msg in self.logs))

    def test_compile_code_failure(self) -> None:
        '''
            Tests compilation abortion when code has validation errors.
        '''
        self.mock_service.should_fail_validation = True
        self.mock_service.diagnostics_to_return = [
            MyCobotDiagnostic(
                line_number=5,
                severity=MyCobotDiagnosticSeverity.ERROR,
                code='ERR_LINT',
                message='Reach exceeded'
            )
        ]

        success, summary, frames = self.coordinator.compile_code('MOVE J1 999.0')
        self.assertFalse(success)
        self.assertIsNone(frames)
        self.assertEqual(len(self.emitted_bytecode), 0)
        self.assertTrue(any(self.constants.msg_compilation_aborted in msg for msg in self.logs))


if __name__ == '__main__':
    main()
