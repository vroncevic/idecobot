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
    Encapsulates core GUI components for simplification of GUI bundle.
'''

from __future__ import annotations

from idecobot.infrastructure.gui.setup.bundle import GUIBundle
from idecobot.infrastructure.gui.setup.dependencies import GUIBundleDependencies
from idecobot.infrastructure.gui.setup.dep_validator import GUIBundleDependenciesValidator
from idecobot.infrastructure.gui.setup.keys import GUIBundleKeys
from idecobot.infrastructure.gui.setup.validator import GUIBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIBundleRegistry:
    '''
        Encapsulates core GUI components for simplification of GUI bundle.

        It defines:

            :methods:
                | create_bundle - Creates a GUI bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: GUIBundleDependencies) -> GUIBundle:
        '''
            Creates a GUI bundle.

            :param dependencies: The GUI bundle dependencies.
            :return: GUI bundle.
            :exceptions:
                | ATSValueError: The GUI bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The GUI bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The GUI bundle must be provided and have proper values.
                | ATSTypeError:  The GUI bundle must be an instance of GUIBundle and
                |                its attributes must be instances of their respective types.
        '''
        GUIBundleDependenciesValidator.validate(dependencies)

        bundle: GUIBundle = GUIBundle(
            service=dependencies[GUIBundleKeys.DEPENDENCY_SERVICE],
            scanner=dependencies[GUIBundleKeys.DEPENDENCY_SCANNER],
            storage=dependencies[GUIBundleKeys.DEPENDENCY_STORAGE],
            root=dependencies[GUIBundleKeys.DEPENDENCY_ROOT],
            menu_bar=dependencies[GUIBundleKeys.DEPENDENCY_MENU_BAR],
            toolbar=dependencies[GUIBundleKeys.DEPENDENCY_TOOLBAR],
            port_panel=dependencies[GUIBundleKeys.DEPENDENCY_PORT_PANEL],
            jog_panel=dependencies[GUIBundleKeys.DEPENDENCY_JOG_PANEL],
            editor_panel=dependencies[GUIBundleKeys.DEPENDENCY_EDITOR_PANEL],
            log_panel=dependencies[GUIBundleKeys.DEPENDENCY_LOG_PANEL],
            status_bar=dependencies[GUIBundleKeys.DEPENDENCY_STATUS_BAR]
        )

        GUIBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version string.
            :exceptions: None.
        '''
        return __version__
