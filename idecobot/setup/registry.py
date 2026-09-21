# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Defines IDECobotBundleRegistry for creating validated idecobot bundles.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from idecobot.core.service.communication.imycobot_streamer import IMyCobotStreamer
from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.icli import ICLI
from idecobot.infrastructure.gui.igui import IGUI
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.dep_validator import IDECobotBundleDependenciesValidator
from idecobot.setup.dependencies import IDECobotBundleDependencies
from idecobot.setup.keys import IDECobotBundleKeys
from idecobot.setup.validator import IDECobotBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleRegistry:
    '''
        Encapsulates validated idecobot bundle creation from dependencies.

        It defines:

            :methods:
                | create_bundle - Creates and validates the idecobot bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: IDECobotBundleDependencies) -> IDECobotBundle:
        '''
            Creates and validates the idecobot bundle.

            :param dependencies: The idecobot bundle dependencies.
            :return: The validated idecobot bundle.
            :exceptions:
                | ATSValueError: If dependencies or bundle validation fails.
                | ATSTypeError: If dependencies or bundle attributes do not match types.
        '''
        IDECobotBundleDependenciesValidator.validate(dependencies)

        base: BaseBundle | None = dependencies.get(IDECobotBundleKeys.DEPENDENCY_BASE) if dependencies else None
        service: IService | None = dependencies.get(IDECobotBundleKeys.DEPENDENCY_SERVICE) if dependencies else None
        gui: IGUI | None = dependencies.get(IDECobotBundleKeys.DEPENDENCY_GUI) if dependencies else None
        streamer: IMyCobotStreamer | None = dependencies.get(IDECobotBundleKeys.DEPENDENCY_STREAMER) if dependencies else None
        cli: ICLI | None = dependencies.get(IDECobotBundleKeys.DEPENDENCY_CLI) if dependencies else None

        bundle: IDECobotBundle = IDECobotBundle(
            base=base,
            service=service,
            gui=gui,
            streamer=streamer,
            cli=cli
        )
        IDECobotBundleValidator.validate(bundle)
        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version string.
            :exceptions: None.
        '''
        return __version__
