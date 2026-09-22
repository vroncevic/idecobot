# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_factory.py
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
    Factory assembling specialized diagnostic readers into DiagnosticsCoordinator.
'''

from __future__ import annotations

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.service.communication.imycobot_controller import IMyCobotController
from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import IMyCobotProtocolCodec
from idecobot.infrastructure.diagnostics.diagnostics_constants import DiagnosticsConstants
from idecobot.infrastructure.diagnostics.diagnostics_coordinator import DiagnosticsCoordinator
from idecobot.infrastructure.diagnostics.joint_diagnostics_reader import JointDiagnosticsReader
from idecobot.infrastructure.diagnostics.servo_diagnostics_reader import ServoDiagnosticsReader
from idecobot.infrastructure.diagnostics.spatial_diagnostics_reader import SpatialDiagnosticsReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsFactory:
    '''
    Factory assembling specialized diagnostic readers into DiagnosticsCoordinator.

    It defines:

        :methods:
            | create_coordinator - Instantiates and wires diagnostics subsystem components.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create_coordinator(
        cls,
        transport: ITransport,
        codec: IMyCobotProtocolCodec,
        controller: IMyCobotController,
        proto: ProtocolConstants,
        constants: DiagnosticsConstants | None = None
    ) -> DiagnosticsCoordinator:
        '''
        Instantiates and wires diagnostics subsystem components.

        :param transport: Injected ITransport communications channel.
        :param codec: Injected IMyCobotProtocolCodec frame encoder/decoder.
        :param controller: Injected IMyCobotController robot controller facade.
        :param proto: Injected ProtocolConstants framing values.
        :param constants: Optional DiagnosticsConstants configuration.
        :return: Fully assembled DiagnosticsCoordinator instance.
        '''
        diag_constants: DiagnosticsConstants = (
            constants if constants is not None else DiagnosticsConstants()
        )

        joint_reader: JointDiagnosticsReader = JointDiagnosticsReader(
            transport=transport,
            codec=codec,
            constants=diag_constants,
            proto=proto
        )
        servo_reader: ServoDiagnosticsReader = ServoDiagnosticsReader(
            transport=transport,
            codec=codec,
            constants=diag_constants,
            proto=proto
        )
        spatial_reader: SpatialDiagnosticsReader = SpatialDiagnosticsReader(
            transport=transport,
            codec=codec,
            constants=diag_constants,
            proto=proto
        )

        return DiagnosticsCoordinator(
            joint_reader=joint_reader,
            servo_reader=servo_reader,
            spatial_reader=spatial_reader,
            controller=controller
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Version string.
        '''
        return __version__

