# -*- coding: UTF-8 -*-

'''
Module
    editor_panel.py
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
    Defines EditorPanel middle-tier DSL editing pane combining editor and controls.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Frame
from tkinter.ttk import Combobox, Label

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.infrastructure.gui.editor.code_editor import CodeEditor
from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.editor.editor_coordinator import EditorCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EditorPanel:
    '''
        Middle-tier DSL editing pane containing toolbar, syntax editor, and diagnostic output.

        It defines:

            :attributes:
                | _frame - Injected outer container Frame widget.
                | _coordinator - Injected EditorCoordinator managing validation/compilation.
                | _editor - Injected CodeEditor widget.
                | _cb_examples - Injected Combobox for template scripts.
                | _lbl_diagnostics - Injected Label displaying diagnostic messages.
                | _constants - Injected EditorConstants design tokens.
            :methods:
                | __init__ - Initializes EditorPanel with injected collaborators.
                | get_frame - Returns container Frame.
                | get_text - Returns editor script text.
                | set_text - Replaces editor script text.
                | clear - Clears editor content.
                | validate_code - Runs semantic validation and updates diagnostics.
                | compile_code - Compiles code and notifies listeners with binary frames.
                | on_example_selected - Loads chosen template script.
                | coordinator - Property returning injected EditorCoordinator.
                | editor - Property returning injected CodeEditor.
                | cb_examples - Property returning injected Combobox.
                | lbl_diagnostics - Property returning injected Label.
                | constants - Property returning injected EditorConstants.
    '''

    _frame: Frame
    _coordinator: EditorCoordinator
    _editor: CodeEditor
    _cb_examples: Combobox
    _lbl_diagnostics: Label
    _constants: EditorConstants

    def __init__(
        self,
        frame: Frame,
        coordinator: EditorCoordinator,
        editor: CodeEditor,
        cb_examples: Combobox,
        lbl_diagnostics: Label,
        constants: EditorConstants
    ) -> None:
        '''
            Initializes EditorPanel composite view with strictly injected dependencies.

            :param frame: Injected container Frame widget.
            :param coordinator: Injected EditorCoordinator instance.
            :param editor: Injected CodeEditor instance.
            :param cb_examples: Injected Combobox instance.
            :param lbl_diagnostics: Injected Label instance for diagnostics.
            :param constants: Injected EditorConstants design tokens.
            :exceptions: None.
        '''
        self._frame = frame
        self._coordinator = coordinator
        self._editor = editor
        self._cb_examples = cb_examples
        self._lbl_diagnostics = lbl_diagnostics
        self._constants = constants

    def get_frame(self) -> Frame:
        '''
            Returns the container frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def get_text(self) -> str:
        '''
            Returns editor script text.

            :return: Code text string.
            :exceptions: None.
        '''
        return self._editor.get_text()

    def set_text(self, content: str) -> None:
        '''
            Replaces editor script text.

            :param content: New script source code.
            :exceptions: None.
        '''
        self._editor.set_text(content)

    def clear(self) -> None:
        '''
            Clears all editor script text.

            :exceptions: None.
        '''
        self._editor.clear()
        self._lbl_diagnostics.config(text=self._constants.status_cleared)

    def validate_code(self) -> bool:
        '''
            Validates current DSL code for syntax and safety rules.

            :return: True if valid with zero errors, False otherwise.
            :exceptions: None.
        '''
        code: str = self.get_text()
        is_valid, summary, _ = self._coordinator.validate_code(code)
        self._lbl_diagnostics.config(text=summary)

        return is_valid

    def compile_code(self) -> Sequence[MyCobotFrame] | None:
        '''
            Compiles current DSL code into binary MyCobotFrames.

            :return: Sequence of compiled frames or None if compilation failed.
            :exceptions: None.
        '''
        code: str = self.get_text()
        success, summary, frames = self._coordinator.compile_code(code)
        self._lbl_diagnostics.config(text=summary)

        return frames if success else None

    def on_example_selected(self) -> None:
        '''
            Event handler for template selection dropdown.

            :exceptions: None.
        '''
        name: str = self._cb_examples.get()
        if name:
            script: str = self._coordinator.load_template(name)
            self._editor.set_text(script)

    @property
    def coordinator(self) -> EditorCoordinator:
        '''
            Returns injected EditorCoordinator.

            :return: EditorCoordinator instance.
        '''
        return self._coordinator

    @property
    def editor(self) -> CodeEditor:
        '''
            Returns injected CodeEditor.

            :return: CodeEditor instance.
        '''
        return self._editor

    @property
    def cb_examples(self) -> Combobox:
        '''
            Returns injected template selector Combobox.

            :return: Combobox instance.
        '''
        return self._cb_examples

    @property
    def lbl_diagnostics(self) -> Label:
        '''
            Returns injected diagnostics Label.

            :return: Label instance.
        '''
        return self._lbl_diagnostics

    @property
    def constants(self) -> EditorConstants:
        '''
            Returns injected EditorConstants.

            :return: EditorConstants instance.
        '''
        return self._constants
