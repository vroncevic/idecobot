# -*- coding: UTF-8 -*-

'''
Module
    example_catalog.py
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
    Defines ExampleCatalog providing pre-configured robot trajectory script templates.
'''

from __future__ import annotations

from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExampleCatalog:
    '''
        Repository of educational and testing DSL example scripts.

        It defines:

            :attributes:
                | EXAMPLES - Mapping of example script names to .cobot source code.
            :methods:
                | get_example_names - Returns list of available example titles.
                | get_example - Retrieves script source text for requested title.
    '''

    EXAMPLES: ClassVar[dict[str, str]] = {
        'Pick and Place': (
            '# myCobot 280 Pick and Place Routine\n'
            'POWER\n'
            'SPEED 30\n'
            'HOME\n'
            'WAIT 1.0\n'
            '# Move to pick position\n'
            'MOVE J1:25.0 J2:15.0 J3:-30.0 J4:10.0 J5:0.0 J6:0.0 SPEED:40\n'
            'WAIT 0.5\n'
            'TOOL GRIP SPEED:50\n'
            'WAIT 1.0\n'
            '# Lift up\n'
            'MOVE J2:0.0 J3:-10.0 SPEED:30\n'
            'WAIT 0.5\n'
            '# Move to place position\n'
            'MOVE J1:-45.0 J2:20.0 J3:-25.0 J4:0.0 J5:0.0 J6:0.0 SPEED:40\n'
            'WAIT 0.5\n'
            'TOOL RELEASE SPEED:50\n'
            'WAIT 1.0\n'
            'HOME\n'
            'RELAX\n'
        ),
        'Cartesian Scan': (
            '# myCobot 280 Cartesian Linear Inspection\n'
            'POWER\n'
            'SPEED 25\n'
            'HOME\n'
            'WAIT 1.0\n'
            'MOVE X:100.0 Y:120.0 Z:150.0 RX:0.0 RY:0.0 RZ:0.0 SPEED:25\n'
            'WAIT 0.5\n'
            'MOVE X:150.0 Y:120.0 Z:150.0 SPEED:20\n'
            'WAIT 0.5\n'
            'MOVE X:150.0 Y:180.0 Z:150.0 SPEED:20\n'
            'WAIT 0.5\n'
            'MOVE X:100.0 Y:180.0 Z:150.0 SPEED:20\n'
            'WAIT 0.5\n'
            'HOME\n'
            'RELAX\n'
        ),
        'Zero Calibration': (
            '# myCobot 280 Home Calibration\n'
            'POWER\n'
            'SPEED 20\n'
            'HOME\n'
            'WAIT 2.0\n'
            'TOOL RELEASE\n'
            'WAIT 1.0\n'
            'RELAX\n'
        )
    }

    @classmethod
    def get_example_names(cls) -> tuple[str, ...]:
        '''
            Returns list of available example titles.

            :return: Tuple of example name strings.
            :exceptions: None.
        '''
        return tuple(cls.EXAMPLES.keys())

    @classmethod
    def get_example(cls, name: str) -> str:
        '''
            Retrieves script source text for requested title.

            :param name: Example title string.
            :return: Script source code string.
            :exceptions: None.
        '''
        return cls.EXAMPLES.get(name, '')
