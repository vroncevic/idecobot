# -*- coding: UTF-8 -*-

'''
Module
    dsl_grammar_constants.py
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
    Defines DslGrammarConstants dataclass for DSL grammar keywords, axes, and tokens.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class DslGrammarConstants:
    '''
        Immutable definition of keywords, axes, tool actions, and parameter tokens for myCobot DSL.

        It defines:

            :attributes:
                | cmd_home - Keyword string for HOME command.
                | cmd_relax - Keyword string for RELAX command.
                | cmd_power - Keyword string for POWER command.
                | cmd_speed - Keyword string for SPEED command.
                | cmd_wait - Keyword string for WAIT command.
                | cmd_tool - Keyword string for TOOL command.
                | cmd_move - Keyword string for MOVE command.
                | commands - Recognized top-level DSL command keywords set.
                | action_grip - Tool action keyword to close gripper.
                | action_release - Tool action keyword to open gripper.
                | tool_actions - Recognized tool action keywords set.
                | default_tool_speed - Default gripper speed percentage.
                | joint_axes - Recognized robotic arm joint axis identifiers set.
                | cartesian_axes - Recognized Cartesian coordinate axis identifiers set.
                | cartesian_coords - Canonical lowercase Cartesian coordinate parameter names.
                | param_value - Generic numeric parameter key string.
                | param_seconds - Duration in seconds parameter key string.
                | param_action - Tool operation action parameter key string.
                | param_speed - Speed percentage parameter key string.
                | param_mode - Motion mode parameter key string.
    '''

    cmd_home: str = 'HOME'
    cmd_relax: str = 'RELAX'
    cmd_power: str = 'POWER'
    cmd_speed: str = 'SPEED'
    cmd_wait: str = 'WAIT'
    cmd_tool: str = 'TOOL'
    cmd_move: str = 'MOVE'
    commands: frozenset[str] = frozenset({
        'HOME', 'RELAX', 'POWER', 'SPEED', 'WAIT', 'TOOL', 'MOVE'
    })

    action_grip: str = 'GRIP'
    action_release: str = 'RELEASE'
    tool_actions: frozenset[str] = frozenset({'GRIP', 'RELEASE'})
    default_tool_speed: float = 50.0

    joint_axes: frozenset[str] = frozenset({'J1', 'J2', 'J3', 'J4', 'J5', 'J6'})
    cartesian_axes: frozenset[str] = frozenset({'X', 'Y', 'Z', 'RX', 'RY', 'RZ'})
    cartesian_coords: tuple[str, ...] = ('x', 'y', 'z', 'rx', 'ry', 'rz')

    param_value: str = 'value'
    param_seconds: str = 'seconds'
    param_action: str = 'action'
    param_speed: str = 'speed'
    param_mode: str = 'mode'
