# -*- coding: UTF-8 -*-

'''
Module
    syntax_highlighter.py
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
    Defines SyntaxHighlighter applying real-time lexical styling to DSL code.
'''

from __future__ import annotations

from re import IGNORECASE, Pattern, compile as re_compile
from tkinter import Text

from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SyntaxHighlighter:
    '''
        Regex-based lexical syntax highlighter for the myCobot .cobot DSL script text.

        It defines:

            :attributes:
                | _re_cmd - Regex for reserved commands.
                | _re_axis - Regex for axis identifiers.
                | _re_num - Regex for numerical literals.
                | _re_comment - Regex for comment lines.
            :methods:
                | __init__ - Configures syntax tags and regex patterns.
                | highlight - Performs full-text lexical styling on target widget.
                | clear_highlights - Clears all syntax color tags from the widget.
    '''

    _re_cmd: Pattern[str] = re_compile(r'\b(MOVE|HOME|TOOL|SPEED|WAIT|POWER|RELAX|GRIP|RELEASE)\b', IGNORECASE)
    _re_axis: Pattern[str] = re_compile(r'\b(J[1-6]|X|Y|Z|RX|RY|RZ|MODE)\b', IGNORECASE)
    _re_num: Pattern[str] = re_compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')
    _re_comment: Pattern[str] = re_compile(r'#[^\r\n]*')

    def __init__(
        self,
        text_widget: Text,
        constants: EditorConstants,
        fonts: FontConfig
    ) -> None:
        '''
            Configures syntax color tags in text widget.

            :param text_widget: Tkinter Text widget to style.
            :param constants: Injected EditorConstants design configuration.
            :param fonts: Injected FontConfig typography tokens.
            :exceptions: None.
        '''
        self._text: Text = text_widget
        self._constants: EditorConstants = constants
        self._fonts: FontConfig = fonts

        self._text.tag_configure(
            'tag_cmd',
            foreground=self._constants.color_keyword,
            font=(self._fonts.family_mono, self._fonts.code[1], 'bold')
        )
        self._text.tag_configure(
            'tag_axis',
            foreground=self._constants.color_command,
            font=self._fonts.code
        )
        self._text.tag_configure(
            'tag_num',
            foreground=self._constants.color_number
        )
        self._text.tag_configure(
            'tag_comment',
            foreground=self._constants.color_comment,
            font=(self._fonts.family_mono, self._fonts.code[1], 'italic')
        )

    def clear_highlights(self) -> None:
        '''
            Clears all syntax color tags across the entire text widget.

            :exceptions: None.
        '''
        for tag in ('tag_cmd', 'tag_axis', 'tag_num', 'tag_comment'):
            self._text.tag_remove(tag, '1.0', 'end')

    def highlight(self) -> None:
        '''
            Performs full-text syntax analysis and tags keywords, axes, numbers, and comments.

            :exceptions: None.
        '''
        content: str = self._text.get('1.0', 'end-1c')
        self.clear_highlights()

        for match in self._re_cmd.finditer(content):
            start: str = f'1.0+{match.start()}c'
            end: str = f'1.0+{match.end()}c'
            self._text.tag_add('tag_cmd', start, end)

        for match in self._re_axis.finditer(content):
            start: str = f'1.0+{match.start()}c'
            end: str = f'1.0+{match.end()}c'
            self._text.tag_add('tag_axis', start, end)

        for match in self._re_num.finditer(content):
            start = f'1.0+{match.start()}c'
            end = f'1.0+{match.end()}c'
            self._text.tag_add('tag_num', start, end)

        for match in self._re_comment.finditer(content):
            start = f'1.0+{match.start()}c'
            end = f'1.0+{match.end()}c'
            self._text.tag_add('tag_comment', start, end)
