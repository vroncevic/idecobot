# -*- coding: UTF-8 -*-

'''
Module
    code_editor.py
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
    Defines CodeEditor composite widget featuring line numbers, syntax highlighting, and undo/redo.
'''

from __future__ import annotations

from tkinter import BOTH, END, LEFT, RIGHT, Y, Frame, Scrollbar, Text

from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.editor.syntax_highlighter import SyntaxHighlighter
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CodeEditor:
    '''
        Syntax-highlighted code editor with synchronized line number gutter.

        It defines:

            :attributes:
                | _constants - Injected EditorConstants design tokens.
                | _palette - Injected ColorPalette color tokens.
                | _fonts - Injected FontConfig typography tokens.
                | _frame - Outer container Frame.
                | _line_numbers - Read-only gutter text widget.
                | _text - Primary editable source code Text widget.
                | _highlighter - SyntaxHighlighter instance.
            :methods:
                | __init__ - Initializes text areas, scrollbars, and highlighting events.
                | get_frame - Returns container Frame.
                | get_text - Returns full editor text content.
                | set_text - Replaces editor text content.
                | clear - Clears editor content.
                | _on_scroll - Synchronizes line numbers with text scroll.
                | _on_content_changed - Updates line numbering and triggers syntax coloring.
    '''

    def __init__(
        self,
        parent: Frame,
        constants: EditorConstants,
        palette: ColorPalette,
        fonts: FontConfig
    ) -> None:
        '''
            Initializes composite code editor.

            :param parent: Parent Frame widget.
            :param constants: Injected EditorConstants design configuration.
            :param palette: Injected ColorPalette color design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :exceptions: None.
        '''
        self._constants: EditorConstants = constants
        self._palette: ColorPalette = palette
        self._fonts: FontConfig = fonts

        self._frame: Frame = Frame(parent, bg=self._palette.bg_canvas)
        self._frame.pack(fill=BOTH, expand=True)

        scrollbar: Scrollbar = Scrollbar(self._frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._line_numbers: Text = Text(
            self._frame,
            width=self._constants.gutter_width,
            padx=4,
            takefocus=0,
            border=0,
            background=self._constants.color_gutter_bg,
            foreground=self._constants.color_gutter_fg,
            state='disabled',
            font=self._fonts.code,
            wrap='none'
        )
        self._line_numbers.pack(side=LEFT, fill=Y)

        self._text: Text = Text(
            self._frame,
            wrap='none',
            undo=True,
            border=0,
            padx=self._constants.padx,
            pady=self._constants.pady,
            background=self._palette.bg_canvas,
            foreground=self._palette.fg_text,
            insertbackground=self._palette.accent_blue,
            font=self._fonts.code,
            selectbackground=self._constants.color_select_bg
        )
        self._text.pack(side=LEFT, fill=BOTH, expand=True)

        self._text.config(yscrollcommand=self._on_scroll)
        scrollbar.config(command=self._text.yview)

        self._highlighter: SyntaxHighlighter = SyntaxHighlighter(
            self._text,
            self._constants,
            self._fonts
        )
        self._text.bind('<KeyRelease>', lambda _: self._on_content_changed())
        self._text.bind('<ButtonRelease-1>', lambda _: self._on_content_changed())
        self._update_line_numbers()

    def get_frame(self) -> Frame:
        '''
            Returns the container frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def _on_scroll(self, first: float, last: float) -> None:
        '''
            Synchronizes gutter scroll with editor scroll.

            :param first: Top fraction.
            :param last: Bottom fraction.
            :exceptions: None.
        '''
        self._line_numbers.yview_moveto(first)

    def _update_line_numbers(self) -> None:
        '''
            Recomputes line numbers for gutter.

            :exceptions: None.
        '''
        lines_count: int = int(self._text.index('end-1c').split('.')[0])
        numbers_str: str = '\n'.join(str(i) for i in range(1, lines_count + 1))
        self._line_numbers.config(state='normal')
        self._line_numbers.delete('1.0', END)
        self._line_numbers.insert('1.0', numbers_str)
        self._line_numbers.config(state='disabled')

    def _on_content_changed(self) -> None:
        '''
            Handles text modification events by updating gutter and styling.

            :exceptions: None.
        '''
        self._update_line_numbers()
        self._highlighter.highlight()

    def get_text(self) -> str:
        '''
            Returns full source code content.

            :return: Code text as string.
            :exceptions: None.
        '''
        return self._text.get('1.0', 'end-1c')

    def set_text(self, content: str) -> None:
        '''
            Replaces editor content and reapplies highlighting.

            :param content: New script source code.
            :exceptions: None.
        '''
        self._text.delete('1.0', END)
        self._text.insert('1.0', content)
        self._on_content_changed()

    def clear(self) -> None:
        '''
            Clears all editor content.

            :exceptions: None.
        '''
        self.set_text('')
