# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Defines IDECobotBundleFactory root composition factory for idecobot.
'''

from __future__ import annotations

from os.path import abspath, dirname, join

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.service.dsl.dsl_service_factory import DslServiceFactory
from idecobot.core.service.dsl.mycobot_dsl_service import MyCobotDslService
from idecobot.core.service.engine import Service
from idecobot.core.service.kinematics.kinematic_validator import KinematicValidator
from idecobot.infrastructure.cli.engine import CLI
from idecobot.infrastructure.cli.setup.factory import CLIBundleFactory
from idecobot.infrastructure.cli.setup.options import CLIBundleOptions
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import MyCobotProtocolCodec
from idecobot.infrastructure.communication.protocol.protocol_codec_factory import ProtocolCodecFactory
from idecobot.infrastructure.communication.streamer.controller_factory import ControllerFactory
from idecobot.infrastructure.communication.streamer.mycobot_controller import MyCobotController
from idecobot.infrastructure.communication.streamer.mycobot_streamer import MyCobotStreamer
from idecobot.infrastructure.communication.streamer.streamer_factory import StreamerFactory
from idecobot.infrastructure.communication.transport.serial_transport import SerialTransport
from idecobot.infrastructure.communication.transport.transport_constants import TransportConstants
from idecobot.infrastructure.gui.engine import IDECobotGUI
from idecobot.setup.bounds_loader import BoundsLoader
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.dependencies import IDECobotBundleDependencies
from idecobot.setup.gui_factory import GUIFactory
from idecobot.setup.keys import IDECobotBundleKeys
from idecobot.setup.opt_validator import IDECobotBundleOptionsValidator
from idecobot.setup.options import IDECobotBundleOptions
from idecobot.setup.registry import IDECobotBundleRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleFactory:
    '''
        Composition root factory assembling all concrete services and adapters.

        It defines:

            :attributes:
                | _info_file - Path to idecobot ATS package configuration file.
            :methods:
                | create_bundle - Creates and wires the complete idecobot application bundle.
                | get_version - Returns factory version string.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'idecobot.cfg'
    )

    @classmethod
    def create_bundle(cls, options: IDECobotBundleOptions | None = None) -> IDECobotBundle:
        '''
            Creates and wires the complete idecobot application bundle.

            :param options: Optional pre-configured bundle options.
            :return: Fully wired IDECobotBundle.
            :exceptions:
                | ATSValueError: If options or dependencies are invalid.
                | ATSTypeError: If types do not match expected interfaces.
        '''
        if options is not None:
            IDECobotBundleOptionsValidator.validate(options)

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=(
                    options[IDECobotBundleKeys.OPTION_INFO_FILE]
                    if options and IDECobotBundleKeys.OPTION_INFO_FILE in options
                    else cls._info_file
                ),
                use_generator=False,
                context_bundle=ContextBundleFactory.create_bundle()
            )
        )

        bounds: MyCobotBounds = BoundsLoader.load(options=options)
        validator: KinematicValidator = KinematicValidator(bounds=bounds)
        protocol_constants: ProtocolConstants = ProtocolConstants()
        grammar: DslGrammarConstants = DslGrammarConstants()
        codec: MyCobotProtocolCodec = ProtocolCodecFactory.create(constants=protocol_constants)
        transport: SerialTransport = SerialTransport(constants=TransportConstants())
        controller: MyCobotController = ControllerFactory.create(
            transport=transport, codec=codec, constants=protocol_constants
        )
        streamer: MyCobotStreamer = StreamerFactory.create(transport=transport, framer=codec.framer)
        dsl_service: MyCobotDslService = DslServiceFactory.create(
            bounds=bounds,
            validator=validator,
            protocol_constants=protocol_constants,
            grammar=grammar
        )

        service: Service = Service(
            bounds=bounds,
            validator=validator,
            dsl_service=dsl_service,
            streamer=streamer,
            controller=controller
        )

        gui: IDECobotGUI = GUIFactory.create(service=service)

        cli: CLI = CLI(
            CLIBundleFactory.create_bundle(
                options=CLIBundleOptions(
                    service=service, parser=base_bundle.option_manager, gui=gui
                )
            )
        )

        return IDECobotBundleRegistry.create_bundle(
            dependencies=IDECobotBundleDependencies(
                base=base_bundle, service=service, gui=gui, streamer=streamer, cli=cli
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: The factory version.
            :exceptions: None.
        '''
        return __version__
