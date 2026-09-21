# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines IDECobotBundle container holding primary application components.
'''

from __future__ import annotations

from dataclasses import dataclass

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.utils.reflection import instance_to_dict

from idecobot.core.service.communication.imycobot_streamer import IMyCobotStreamer
from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.icli import ICLI
from idecobot.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class IDECobotBundle:
    '''
        Container holding all primary application components for idecobot.

        It defines:

            :attributes:
                | base - Base ATS bundle with logger, options, and info managers.
                | service - Core robot service facade.
                | gui - GUI presentation adapter.
                | streamer - Robot communication streamer.
                | cli - Command line interface adapter.
            :methods:
                | to_dict - Converts the bundle to a dictionary.
    '''

    base: BaseBundle
    service: IService
    gui: IGUI
    streamer: IMyCobotStreamer
    cli: ICLI

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the bundle to a dictionary representation.

            :return: Dictionary representation of the bundle.
            :exceptions: None.
        '''
        return instance_to_dict(self)
