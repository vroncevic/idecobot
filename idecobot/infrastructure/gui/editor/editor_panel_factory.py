# -*- coding: UTF-8 -*-

'''
Module
    editor_panel_factory.py
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
    Defines EditorPanelFactory responsible for assembling EditorPanel and wiring controls.
'''

from __future__ import annotations

from collections.abc import Callable, Sequence
from tkinter import BOTH, Frame, LEFT, RIGHT, X
from tkinter.ttk import Button, Combobox, Label

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.service.dsl.imycobot_dsl_service import IMyCobotDslService
from idecobot.infrastructure.gui.editor.code_editor import CodeEditor
from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.editor.editor_coordinator import EditorCoordinator
from idecobot.infrastructure.gui.editor.editor_panel import EditorPanel
from idecobot.infrastructure.gui.editor.example_catalog import ExampleCatalog
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EditorPanelFactory:
    '''
        Factory assembling EditorPanel composite view and wiring header controls.

        It defines:

            :methods:
                | create_editor_panel - Constructs frame, controls, coordinator, and EditorPanel.
    '''

    @classmethod
    def create_editor_panel(
        cls,
        parent: Frame,
        dsl_service: IMyCobotDslService,
        on_bytecode: Callable[[Sequence[MyCobotFrame]], None],
        on_log: Callable[[str], None],
        palette: ColorPalette,
        fonts: FontConfig,
        constants: EditorConstants
    ) -> EditorPanel:
        '''
            Constructs and wires the EditorPanel composite view with all controls.

            :param parent: Parent container Frame.
            :param dsl_service: Injected IMyCobotDslService domain abstraction.
            :param on_bytecode: Callback receiving compiled bytecode frames.
            :param on_log: Logging callback.
            :param palette: Injected ColorPalette design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected EditorConstants configuration.
            :return: Fully assembled EditorPanel instance.
            :exceptions: None.
        '''
        coordinator: EditorCoordinator = EditorCoordinator(
            dsl_service=dsl_service,
            on_bytecode=on_bytecode,
            on_log=on_log,
            constants=constants
        )

        frame: Frame = Frame(
            parent,
            bg=palette.bg_card,
            padx=constants.padx,
            pady=constants.pady
        )
        frame.pack(
            fill=BOTH,
            expand=True,
            padx=constants.frame_padx,
            pady=constants.frame_pady
        )

        header: Frame = Frame(frame, bg=palette.bg_card)
        header.pack(fill=X, pady=constants.header_pady)

        lbl_title: Label = Label(
            header,
            text=constants.title_text,
            style=constants.style_header
        )
        lbl_title.pack(side=LEFT, padx=constants.title_padx)

        btn_val: Button = Button(
            header,
            text=constants.btn_validate_text,
            style=constants.style_accent_btn
        )
        btn_val.pack(side=LEFT, padx=constants.btn_padx)

        btn_comp: Button = Button(header, text=constants.btn_compile_text)
        btn_comp.pack(side=LEFT, padx=constants.btn_padx)

        lbl_ex: Label = Label(
            header,
            text=constants.template_label,
            style=constants.style_label
        )
        lbl_ex.pack(side=LEFT, padx=constants.template_padx)

        cb_examples: Combobox = Combobox(
            header,
            values=list(coordinator.get_available_templates()),
            width=constants.examples_width,
            state=constants.state_readonly
        )
        cb_examples.pack(side=LEFT, padx=constants.examples_padx)

        btn_clear: Button = Button(header, text=constants.btn_clear_text)
        btn_clear.pack(side=RIGHT, padx=constants.btn_padx)

        editor: CodeEditor = CodeEditor(frame, constants, palette, fonts)

        lbl_diagnostics: Label = Label(
            frame,
            text=constants.status_ready,
            style=constants.style_status
        )
        lbl_diagnostics.pack(fill=X, pady=constants.diagnostics_pady)

        panel: EditorPanel = EditorPanel(
            frame=frame,
            coordinator=coordinator,
            editor=editor,
            cb_examples=cb_examples,
            lbl_diagnostics=lbl_diagnostics,
            constants=constants
        )

        btn_val.config(command=panel.validate_code)
        btn_comp.config(command=panel.compile_code)
        btn_clear.config(command=panel.clear)
        cb_examples.bind(
            constants.event_combobox_selected,
            lambda _: panel.on_example_selected()
        )

        default_ex: str = ExampleCatalog.get_example(constants.default_example)
        editor.set_text(default_ex)

        return panel
