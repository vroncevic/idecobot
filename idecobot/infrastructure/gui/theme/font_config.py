# -*- coding: UTF-8 -*-

'''
Module
    font_config.py
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
    Defines FontConfig dataclass standardizing UI typography tokens.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class FontConfig:
    '''
        Immutable typography tokens holding font families and specifications.

        It defines:

            :attributes:
                | family - Standard sans-serif font family name.
                | family_mono - Monospaced font family name.
                | title - Small bold section title font tuple.
                | header - Large bold header label font tuple.
                | body - Regular body text and entry font tuple.
                | body_bold - Bold body and button font tuple.
                | status - Monospaced status line font tuple.
                | status_bold - Bold connection status indicator font tuple.
                | code - Monospaced editor font tuple.
    '''

    family: str = 'DejaVu Sans'
    family_mono: str = 'DejaVu Sans Mono'
    title: tuple[str, int, str] = ('DejaVu Sans', 8, 'bold')
    header: tuple[str, int, str] = ('DejaVu Sans', 10, 'bold')
    body: tuple[str, int] = ('DejaVu Sans', 9)
    body_bold: tuple[str, int, str] = ('DejaVu Sans', 9, 'bold')
    status: tuple[str, int] = ('DejaVu Sans Mono', 9)
    status_bold: tuple[str, int, str] = ('DejaVu Sans', 9, 'bold')
    code: tuple[str, int] = ('DejaVu Sans Mono', 10)
