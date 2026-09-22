# -*- coding: UTF-8 -*-

'''
Module
    igui.py
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
    Defines structural interface protocol IGUI for graphical user interface adapters.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGUI(Protocol):
    '''
        Structural interface protocol for idecobot GUI presentation adapters.

        It defines:

            :methods:
                | is_initialized - Checks if the GUI adapter is properly initialized.
                | start - Starts the GUI main event loop.
                | stop - Closes and destroys the GUI window.
                | load_file - Loads an initial DSL script file into the editor.
                | connect_port - Sets and connects to specified communications port.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if the GUI adapter is properly initialized.

            :return: True if initialized, False otherwise.
        '''

    def start(self) -> None:
        '''
            Starts the GUI main event loop.
        '''

    def stop(self) -> None:
        '''
            Closes and destroys the GUI window.
        '''

    def load_file(self, filepath: str) -> None:
        '''
            Loads an initial DSL script file into the editor.

            :param filepath: Path to the .cobot script file.
        '''

    def connect_port(self, port: str) -> bool:
        '''
            Sets and connects to specified communications port.

            :param port: Serial device path string.
            :return: True if connected, False otherwise.
        '''


