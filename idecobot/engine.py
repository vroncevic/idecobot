# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Engine orchestrating the initialization and execution of idecobot.
'''

from __future__ import annotations

from collections.abc import Mapping
from logging import ERROR, INFO
from sys import stdout

from ats_utilities.base.engine import Base
from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.logger.ilogger import ILogger

from idecobot.infrastructure.cli.icli import ICLI
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.validator import IDECobotBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobot(Base):
    '''
        Engine orchestrating the initialization and execution of idecobot.

        It defines:

            :attributes:
                | _is_initialized - Flag indicating whether the idecobot engine is initialized.
                | _logger - Logger for logging messages during lifecycle and execution.
                | _cli - Injected command line interface adapter.
            :methods:
                | __init__ - Initializes the idecobot engine with bundle adapters and services.
                | process - Executes the idecobot CLI command.
    '''

    _is_initialized: bool
    _logger: ILogger
    _cli: ICLI

    def __init__(self, bundle: IDECobotBundle) -> None:
        '''
            Initializes the idecobot engine with adapters and services.

            :param bundle: The idecobot bundle containing adapters and services.
            :exceptions:
                | ATSValueError: If bundle validation fails.
                | ATSTypeError:  If bundle types do not match requirements.
        '''
        self._is_initialized = False

        try:
            IDECobotBundleValidator.validate(bundle)

            # Initialize base engine
            super().__init__(bundle.base)
            self._logger = self.get_context().logger

            # Mark as not initialized (waiting for other components to be initialized)
            self._is_initialized = False

            # Setting up primary inbound adapter (CLI interface)
            self._cli = bundle.cli

            # Mark as initialized (all components initialized)
            self._is_initialized = all(
                component.is_initialized() for component in [
                    bundle.base.option_manager,
                    bundle.service,
                    bundle.gui,
                    self._cli
                ] if component
            )
            self._logger.write_log(INFO, '✅ idecobot: engine initialized successfully!')

        except (ATSValueError, ATSTypeError) as exc:
            stdout.write(f'❌ idecobot: {exc}!\n')

        except Exception as exc:
            stdout.write(f'❌ idecobot unexpected exception: {exc}!\n')

    def process(self, verbose: bool = False) -> bool:
        '''
            Processes the idecobot commands.

            :param verbose: Enable verbose logging output.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''
        result: Mapping[str, object] = {}

        try:
            if self.is_initialized():
                self._logger.write_log(INFO, '🔥 Starting execution command...')
                result = self._cli.run()
                self._logger.write_log(INFO, '✅ Execution finished!')

                if result.get('returncode') != 0:
                    self._logger.write_log(ERROR, f'❌ idecobot: {result.get("stderr") or "failed!"}')
                    return False

                self._logger.write_log(INFO, '✅ idecobot: done!')
                self._logger.write_log(INFO, '✅ idecobot: exiting successfully!')
                return True

            self._logger.write_log(ERROR, '❌ idecobot: engine not initialized!')
            return False

        except (ATSValueError, ATSTypeError) as exc:
            self._logger.write_log(ERROR, f'❌ idecobot: {exc}!')
            return False

        except Exception as exc:
            self._logger.write_log(ERROR, f'❌ idecobot unexpected exception: {exc}!')
            return False
