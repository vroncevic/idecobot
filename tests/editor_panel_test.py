# -*- coding: UTF-8 -*-

'''
Module
    editor_panel_test.py
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
    Unit tests for EditorPanel and EditorPanelFactory.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Frame, Tk
from unittest import TestCase, main

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import (
    MyCobotDiagnostic,
)
from idecobot.infrastructure.gui.editor.code_editor import CodeEditor
from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.editor.editor_coordinator import (
    EditorCoordinator,
)
from idecobot.infrastructure.gui.editor.editor_panel import EditorPanel
from idecobot.infrastructure.gui.editor.editor_panel_factory import (
    EditorPanelFactory,
)
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockDslService:
    '''
        Mock DSL service for editor panel testing.
    '''

    def tokenize(self, code: str):
        return ()

    def parse(self, tokens):
        return MyCobotProgram(instructions=())

    def lint(self, program):
        return ()

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        return [MyCobotFrame(cmd_id=0x20, payload=bytes([0x01]), delay_after_sec=0.0)]

    def validate(
        self,
        code: str
    ) -> tuple[MyCobotProgram | None, Sequence[MyCobotDiagnostic]]:
        return MyCobotProgram(instructions=()), []


class MockWorkspaceService:
    '''
        Mock workspace service for editor panel testing.
    '''

    def __init__(self) -> None:
        self.workspace_dir: str = '/workspace'
        self.scripts: list[str] = [
            '10_routine_pick_and_place.cobot',
            '01_cmd_power.cobot'
        ]

    def ensure_workspace(self) -> str:
        return self.workspace_dir

    def get_workspace_dir(self) -> str:
        return self.workspace_dir

    def list_scripts(self) -> list[str]:
        return sorted(self.scripts)

    def extract_examples(self, force: bool = False) -> bool:
        return True

    def get_version(self) -> str:
        return '1.0.3'


class MockStorageService:
    '''
        Mock storage service for editor panel testing.
    '''

    def __init__(self) -> None:
        self.files: dict[str, str] = {
            '/workspace/10_routine_pick_and_place.cobot': 'MOVE J1 10.0\nWAIT 1.0\n',
            '/workspace/01_cmd_power.cobot': 'POWER\nWAIT 1.0\n'
        }

    def load_script(self, path: str) -> str:
        if path in self.files:
            return self.files[path]
        raise OSError(f'File not found: {path}')

    def save_script(self, path: str, content: str) -> bool:
        self.files[path] = content
        return True


class TestEditorPanel(TestCase):
    '''
        Unit tests for EditorPanel composite view and EditorPanelFactory.

        It defines:

            :methods:
                | setUp - Initializes Tk root and collaborators.
                | tearDown - Destroys root window.
                | test_factory_assembly - Verifies factory assembly and initial template.
                | test_validation_and_compilation - Verifies validate and compile panel actions.
                | test_example_selection - Verifies template switching from combobox.
                | test_clear_and_set_text - Verifies text manipulation and clear action.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.frame: Frame = Frame(self.root)
        self.frame.pack()
        self.dsl_service: MockDslService = MockDslService()
        self.workspace_service: MockWorkspaceService = MockWorkspaceService()
        self.storage: MockStorageService = MockStorageService()
        self.palette: ColorPalette = ColorPalette()
        self.fonts: FontConfig = FontConfig()
        self.constants: EditorConstants = EditorConstants()
        self.bytecode_emitted: list[Sequence[MyCobotFrame]] = []
        self.logs: list[str] = []

    def tearDown(self) -> None:
        '''
            Destroys root Tk window.
        '''
        self.root.destroy()

    def create_panel(self) -> EditorPanel:
        '''
            Creates an EditorPanel instance via EditorPanelFactory.
        '''
        return EditorPanelFactory.create_editor_panel(
            parent=self.frame,
            dsl_service=self.dsl_service,
            workspace_service=self.workspace_service,
            storage=self.storage,
            on_bytecode=self.bytecode_emitted.append,
            on_log=self.logs.append,
            palette=self.palette,
            fonts=self.fonts,
            constants=self.constants
        )

    def test_factory_assembly(self) -> None:
        '''
            Verifies factory properly configures components and loads initial template.
        '''
        panel: EditorPanel = self.create_panel()
        self.assertIsInstance(panel, EditorPanel)
        self.assertIsInstance(panel.get_frame(), Frame)
        self.assertIsInstance(panel.coordinator, EditorCoordinator)
        self.assertIsInstance(panel.editor, CodeEditor)
        self.assertEqual(panel.constants, self.constants)
        self.assertIn('MOVE J1 10.0', panel.get_text())
        self.assertEqual(panel.cb_examples.get(), '10_routine_pick_and_place.cobot')

    def test_validation_and_compilation(self) -> None:
        '''
            Verifies code validation and compilation actions.
        '''
        panel: EditorPanel = self.create_panel()
        is_valid: bool = panel.validate_code()
        self.assertTrue(is_valid)

        frames: Sequence[MyCobotFrame] | None = panel.compile_code()
        self.assertIsNotNone(frames)
        self.assertEqual(len(self.bytecode_emitted), 1)

    def test_example_selection(self) -> None:
        '''
            Verifies selecting a different template updates editor text.
        '''
        panel: EditorPanel = self.create_panel()
        panel.cb_examples.set('01_cmd_power.cobot')
        panel.on_example_selected()
        self.assertIn('POWER', panel.get_text())

    def test_clear_and_set_text(self) -> None:
        '''
            Verifies clear and set_text operations.
        '''
        panel: EditorPanel = self.create_panel()
        panel.clear()
        self.assertEqual(panel.get_text().strip(), '')

        panel.set_text('HOME 50')
        self.assertEqual(panel.get_text().strip(), 'HOME 50')


if __name__ == '__main__':
    main()
