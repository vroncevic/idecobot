# -*- coding: UTF-8 -*-

'''
Module
    editor_coordinator.py
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
    Defines EditorCoordinator managing DSL validation, compilation, and template loading.
'''

from __future__ import annotations

from collections.abc import Callable, Sequence
from os.path import join

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import MyCobotDiagnosticSeverity
from idecobot.core.service.dsl.imycobot_dsl_service import IMyCobotDslService
from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService
from idecobot.infrastructure.storage.iworkspace_service import IWorkspaceService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EditorCoordinator:
    '''
        Coordinates DSL program validation, bytecode compilation, and example templates.

        It defines:

            :attributes:
                | _dsl_service - Injected domain DSL service abstraction.
                | _workspace_service - Injected user workspace service abstraction.
                | _storage - Injected script storage service abstraction.
                | _on_bytecode - Injected callback receiving compiled robot frames.
                | _on_log - Injected logging callback.
                | _constants - Injected EditorConstants configuration.
            :methods:
                | __init__ - Initializes editor coordinator with collaborators.
                | validate_code - Validates DSL source code and reports diagnostics.
                | compile_code - Compiles valid DSL code into binary MyCobotFrames.
                | load_template - Fetches example script text from workspace.
                | get_available_templates - Returns list of available workspace scripts.
                | workspace_service - Property returning injected IWorkspaceService.
                | storage - Property returning injected IScriptStorageService.
                | constants - Property returning injected EditorConstants.
    '''

    _dsl_service: IMyCobotDslService
    _workspace_service: IWorkspaceService
    _storage: IScriptStorageService
    _on_bytecode: Callable[[Sequence[MyCobotFrame]], None]
    _on_log: Callable[[str], None]
    _constants: EditorConstants

    def __init__(
        self,
        dsl_service: IMyCobotDslService,
        workspace_service: IWorkspaceService,
        storage: IScriptStorageService,
        on_bytecode: Callable[[Sequence[MyCobotFrame]], None],
        on_log: Callable[[str], None],
        constants: EditorConstants
    ) -> None:
        '''
            Initializes editor coordinator.

            :param dsl_service: Injected IMyCobotDslService abstraction.
            :param workspace_service: Injected IWorkspaceService abstraction.
            :param storage: Injected IScriptStorageService abstraction.
            :param on_bytecode: Injected callback receiving compiled robot frames.
            :param on_log: Injected logging callback.
            :param constants: Injected EditorConstants configuration.
            :exceptions: None.
        '''
        self._dsl_service = dsl_service
        self._workspace_service = workspace_service
        self._storage = storage
        self._on_bytecode = on_bytecode
        self._on_log = on_log
        self._constants = constants

    def validate_code(
        self,
        code: str
    ) -> tuple[bool, str, Sequence[MyCobotDiagnostic]]:
        '''
            Validates DSL source code for syntactic and semantic correctness.

            :param code: Source code string to validate.
            :return: Tuple of (is_valid, summary_message, diagnostics).
            :exceptions: None.
        '''
        program, diagnostics = self._dsl_service.validate(code)
        has_errors: bool = any(
            d.severity == MyCobotDiagnosticSeverity.ERROR for d in diagnostics
        )

        if program is not None and not has_errors:
            self._on_log(self._constants.msg_log_validation_passed)

            return True, self._constants.msg_validation_passed, diagnostics

        errors_count: int = sum(
            1 for d in diagnostics if d.severity == MyCobotDiagnosticSeverity.ERROR
        )
        warns_count: int = len(diagnostics) - errors_count

        if diagnostics:
            first: MyCobotDiagnostic = diagnostics[0]
            summary: str = (
                f'❌ Line {first.line_number} [{first.code}]: {first.message} '
                f'(Total: {errors_count} err, {warns_count} warn)'
            )

            for diag in diagnostics:
                prefix: str = (
                    self._constants.prefix_error
                    if diag.severity == MyCobotDiagnosticSeverity.ERROR
                    else self._constants.prefix_warn
                )
                self._on_log(
                    f'{prefix} [Line {diag.line_number}] [{diag.code}]: {diag.message}'
                )

            return False, summary, diagnostics

        return False, self._constants.msg_validation_failed, diagnostics

    def compile_code(self, code: str) -> tuple[bool, str, Sequence[MyCobotFrame] | None]:
        '''
            Compiles DSL source code into executable binary MyCobotFrames.

            :param code: Source code string to compile.
            :return: Tuple of (success, summary_message, compiled_frames_or_none).
            :exceptions: None.
        '''
        program, diagnostics = self._dsl_service.validate(code)
        has_errors: bool = any(
            d.severity == MyCobotDiagnosticSeverity.ERROR for d in diagnostics
        )

        if program is None or has_errors:
            _, summary, _ = self.validate_code(code)
            self._on_log(self._constants.msg_compilation_aborted)

            return False, summary, None

        frames: Sequence[MyCobotFrame] = self._dsl_service.compile(program)

        self._on_bytecode(frames)
        self._on_log(f'⚙ Successfully compiled {len(frames)} binary robot frames.')

        return True, self._constants.msg_validation_passed, frames

    def load_template(self, name: str) -> str:
        '''
            Loads template script text from user workspace by filename.

            :param name: Template script filename.
            :return: Source code string of template.
            :exceptions: None.
        '''
        file_path: str = join(self._workspace_service.get_workspace_dir(), name)
        try:
            script: str = self._storage.load_script(file_path)
            self._on_log(f'{self._constants.log_template_loaded} {name}')

            return script

        except (OSError, ValueError) as err:
            self._on_log(
                f'{self._constants.prefix_error}: Failed to load template {name}: {err}'
            )

            return ''

    def get_available_templates(self) -> Sequence[str]:
        '''
            Returns names of all available example templates from workspace.

            :return: Sequence of template filename strings.
            :exceptions: None.
        '''
        return self._workspace_service.list_scripts()

    @property
    def workspace_service(self) -> IWorkspaceService:
        '''
            Returns injected IWorkspaceService.

            :return: IWorkspaceService instance.
        '''
        return self._workspace_service

    @property
    def storage(self) -> IScriptStorageService:
        '''
            Returns injected IScriptStorageService.

            :return: IScriptStorageService instance.
        '''
        return self._storage

    @property
    def constants(self) -> EditorConstants:
        '''
            Returns injected EditorConstants.

            :return: EditorConstants instance.
        '''
        return self._constants
