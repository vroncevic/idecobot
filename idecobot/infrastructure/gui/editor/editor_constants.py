# -*- coding: UTF-8 -*-

'''
Module
    editor_constants.py
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
    Defines EditorConstants frozen dataclass for DSL editor views.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class EditorConstants:
    '''
        Constants for editor panel layout, syntax highlighting, styles, and diagnostic messages.

        It defines:

            :attributes:
                | tab_size - Number of spaces representing an indentation level.
                | insert_width - Cursor pixel thickness.
                | gutter_width - Line numbers gutter character width.
                | padx - Editor text widget internal horizontal margin.
                | pady - Editor text widget internal vertical margin.
                | color_keyword - Syntax highlighting color for DSL keywords.
                | color_command - Syntax highlighting color for top-level commands.
                | color_number - Syntax highlighting color for numeric literals.
                | color_comment - Syntax highlighting color for comment lines.
                | color_ident - Syntax highlighting color for parameter identifiers.
                | color_cursor - Caret cursor accent color.
                | color_select_bg - Text selection background color.
                | color_gutter_bg - Line number gutter background color.
                | color_gutter_fg - Line number gutter text foreground color.
                | title_text - Panel header title label text.
                | btn_validate_text - Validation button caption.
                | btn_compile_text - Compilation button caption.
                | btn_clear_text - Clear editor button caption.
                | template_label - Template dropdown label caption.
                | status_ready - Default ready diagnostic label text.
                | status_cleared - Diagnostic text after clearing editor.
                | default_example - Default template script name to load.
                | examples_width - Combobox width in characters.
                | header_pady - Header panel vertical padding tuple.
                | title_padx - Title label horizontal padding tuple.
                | btn_padx - Action button horizontal padding.
                | template_padx - Template label horizontal padding tuple.
                | examples_padx - Template combobox horizontal padding.
                | diagnostics_pady - Diagnostics label vertical padding tuple.
                | frame_padx - Main panel horizontal margin.
                | frame_pady - Main panel vertical margin.
                | style_header - Ttk style identifier for editor title label.
                | style_accent_btn - Ttk style identifier for accent action button.
                | style_label - Ttk style identifier for standard labels.
                | style_status - Ttk style identifier for diagnostics readout.
                | event_combobox_selected - Virtual event string for combobox selection.
                | state_readonly - State string for non-editable comboboxes.
                | msg_validation_passed - Diagnostic label text when verification succeeds.
                | msg_log_validation_passed - Log message when verification succeeds.
                | msg_compilation_aborted - Log message when compilation is aborted.
                | msg_validation_failed - Diagnostic label text on empty or unparseable code.
                | prefix_error - Log line prefix for error diagnostics.
                | prefix_warn - Log line prefix for warning diagnostics.
                | log_template_loaded - Log line prefix when template is loaded.
    '''

    tab_size: int = 4
    insert_width: int = 2
    gutter_width: int = 4
    padx: int = 6
    pady: int = 4
    color_keyword: str = '#c678dd'
    color_command: str = '#61afef'
    color_number: str = '#d19a66'
    color_comment: str = '#5c6370'
    color_ident: str = '#e5c07b'
    color_cursor: str = '#528bff'
    color_select_bg: str = '#3e4451'
    color_gutter_bg: str = '#21252b'
    color_gutter_fg: str = '#5c6370'
    title_text: str = 'myCobot 280 DSL Editor'
    btn_validate_text: str = '✓ Validate'
    btn_compile_text: str = '⚙ Compile'
    btn_clear_text: str = 'Clear'
    template_label: str = 'Template:'
    status_ready: str = 'Ready. Write DSL script and click Validate.'
    status_cleared: str = 'Editor cleared.'
    default_example: str = 'Pick and Place'
    examples_width: int = 18
    header_pady: tuple[int, int] = (0, 4)
    title_padx: tuple[int, int] = (0, 10)
    btn_padx: int = 3
    template_padx: tuple[int, int] = (10, 2)
    examples_padx: int = 2
    diagnostics_pady: tuple[int, int] = (4, 0)
    frame_padx: int = 4
    frame_pady: int = 2
    style_header: str = 'Header.TLabel'
    style_accent_btn: str = 'Accent.TButton'
    style_label: str = 'TLabel'
    style_status: str = 'Status.TLabel'
    event_combobox_selected: str = '<<ComboboxSelected>>'
    state_readonly: str = 'readonly'
    msg_validation_passed: str = '✅ Validation passed: 0 errors, safe motion.'
    msg_log_validation_passed: str = '✅ DSL validation passed with 0 errors.'
    msg_compilation_aborted: str = '❌ Compilation aborted due to validation errors.'
    msg_validation_failed: str = '❌ Validation failed: empty or unparseable program.'
    prefix_error: str = '❌ ERROR'
    prefix_warn: str = '⚠️ WARN'
    log_template_loaded: str = 'Loaded template:'
