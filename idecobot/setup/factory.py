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

from json import loads
from os.path import abspath, dirname, exists, join

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.communication.serial_defaults import SerialDefaults
from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.service.dsl.compiler.mycobot_compiler import MyCobotCompiler
from idecobot.core.service.dsl.lexer.mycobot_lexer import MyCobotLexer
from idecobot.core.service.dsl.linter.mycobot_linter import MyCobotLinter
from idecobot.core.service.dsl.linter.rules.ground_safety_rule import GroundSafetyRule
from idecobot.core.service.dsl.linter.rules.jerk_limit_rule import JerkLimitRule
from idecobot.core.service.dsl.linter.rules.joint_bounds_rule import JointBoundsRule
from idecobot.core.service.dsl.linter.rules.speed_limit_rule import SpeedLimitRule
from idecobot.core.service.dsl.linter.rules.workspace_reach_rule import WorkspaceReachRule
from idecobot.core.service.dsl.mycobot_dsl_service import MyCobotDslService
from idecobot.core.service.dsl.parser.commands.home_command_parser import HomeCommandParser
from idecobot.core.service.dsl.parser.commands.move_command_parser import MoveCommandParser
from idecobot.core.service.dsl.parser.commands.power_command_parser import PowerCommandParser
from idecobot.core.service.dsl.parser.commands.relax_command_parser import RelaxCommandParser
from idecobot.core.service.dsl.parser.commands.speed_command_parser import SpeedCommandParser
from idecobot.core.service.dsl.parser.commands.tool_command_parser import ToolCommandParser
from idecobot.core.service.dsl.parser.commands.wait_command_parser import WaitCommandParser
from idecobot.core.service.dsl.parser.mycobot_parser import MyCobotParser
from idecobot.core.service.engine import Service
from idecobot.infrastructure.cli.engine import CLI
from idecobot.infrastructure.cli.setup.bundle import CLIBundle
from idecobot.infrastructure.cli.setup.factory import CLIBundleFactory
from idecobot.infrastructure.cli.setup.options import CLIBundleOptions
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import MyCobotProtocolCodec
from idecobot.infrastructure.communication.serial_port_scanner import SerialPortScanner
from idecobot.infrastructure.communication.streamer.mycobot_controller import MyCobotController
from idecobot.infrastructure.communication.streamer.mycobot_streamer import MyCobotStreamer
from idecobot.infrastructure.communication.transport.serial_transport import SerialTransport
from idecobot.infrastructure.gui.engine import IDECobotGUI
from idecobot.infrastructure.gui.engine_constants import EngineConstants
from idecobot.infrastructure.gui.setup.bundle import GUIBundle
from idecobot.infrastructure.gui.setup.factory import GUIBundleFactory
from idecobot.infrastructure.gui.setup.gui_event_handler import GUIEventHandler
from idecobot.infrastructure.gui.setup.keys import GUIBundleKeys
from idecobot.infrastructure.gui.setup.options import GUIBundleOptions
from idecobot.infrastructure.storage.script_storage_service import ScriptStorageService
from idecobot.infrastructure.storage.storage_constants import StorageConstants
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.dependencies import IDECobotBundleDependencies
from idecobot.setup.keys import IDECobotBundleKeys
from idecobot.setup.opt_validator import IDECobotBundleOptionsValidator
from idecobot.setup.options import IDECobotBundleOptions
from idecobot.setup.registry import IDECobotBundleRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleFactory:
    '''
        Composition root factory assembling all concrete services and adapters.

        It defines:

            :attributes:
                | _info_file - Path to idecobot ATS package configuration file.
                | _geometry_config_file - Path to robot kinematic boundaries JSON.
            :methods:
                | _resolve_bounds - Constructs MyCobotBounds from config file and options.
                | create_bundle - Creates and wires the complete idecobot application bundle.
                | get_version - Returns factory version string.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'idecobot.cfg'
    )
    _geometry_config_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'mycobot_geometry.json'
    )

    @classmethod
    def _resolve_bounds(
        cls,
        options: IDECobotBundleOptions | None = None
    ) -> MyCobotBounds:
        '''
            Constructs MyCobotBounds from config file and options.

            :param options: Optional bundle configuration options.
            :return: MyCobotBounds domain model.
            :exceptions: None.
        '''
        config_path: str = cls._geometry_config_file
        if options and IDECobotBundleKeys.OPTION_ROBOT_CONFIG in options:
            config_path = str(options[IDECobotBundleKeys.OPTION_ROBOT_CONFIG])

        data: dict[str, object] = {}

        if exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as handle:
                    data = loads(handle.read())

            except (OSError, ValueError):
                data = {}

        return MyCobotBounds.from_dict(data=data)

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

        info_file: str = (
            options[IDECobotBundleKeys.OPTION_INFO_FILE]
            if options and IDECobotBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()
        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        bounds: MyCobotBounds = cls._resolve_bounds(options=options)
        protocol_constants: ProtocolConstants = ProtocolConstants()
        grammar: DslGrammarConstants = DslGrammarConstants()
        serial_defaults: SerialDefaults = SerialDefaults()
        codec: MyCobotProtocolCodec = MyCobotProtocolCodec(constants=protocol_constants)
        transport: SerialTransport = SerialTransport(defaults=serial_defaults)
        controller: MyCobotController = MyCobotController(
            transport=transport,
            codec=codec,
            constants=protocol_constants
        )
        streamer: MyCobotStreamer = MyCobotStreamer(transport=transport)
        scanner: SerialPortScanner = SerialPortScanner()
        storage_constants: StorageConstants = StorageConstants()
        storage: ScriptStorageService = ScriptStorageService(constants=storage_constants)

        command_parsers = [
            HomeCommandParser(),
            RelaxCommandParser(),
            PowerCommandParser(),
            SpeedCommandParser(),
            WaitCommandParser(),
            ToolCommandParser(grammar=grammar),
            MoveCommandParser(grammar=grammar)
        ]
        lexer: MyCobotLexer = MyCobotLexer(grammar=grammar)
        parser: MyCobotParser = MyCobotParser(parsers=command_parsers)
        lint_rules = [
            JointBoundsRule(bounds=bounds),
            WorkspaceReachRule(bounds=bounds),
            GroundSafetyRule(bounds=bounds),
            JerkLimitRule(bounds=bounds),
            SpeedLimitRule(bounds=bounds)
        ]
        linter: MyCobotLinter = MyCobotLinter(rules=lint_rules)
        compiler: MyCobotCompiler = MyCobotCompiler(
            constants=protocol_constants,
            default_speed=bounds.default_speed
        )
        dsl_service: MyCobotDslService = MyCobotDslService(
            lexer=lexer,
            parser=parser,
            linter=linter,
            compiler=compiler
        )

        service: Service = Service(
            bounds=bounds,
            dsl_service=dsl_service,
            streamer=streamer,
            controller=controller
        )

        gui_handler: GUIEventHandler = GUIEventHandler()
        gui_options: GUIBundleOptions = {
            GUIBundleKeys.OPTION_SERVICE: service,
            GUIBundleKeys.OPTION_SCANNER: scanner,
            GUIBundleKeys.OPTION_STORAGE: storage
        }
        gui_bundle: GUIBundle = GUIBundleFactory.create_bundle(
            options=gui_options,
            handler=gui_handler
        )
        gui_constants: EngineConstants = EngineConstants()
        gui: IDECobotGUI = IDECobotGUI(
            bundle=gui_bundle,
            constants=gui_constants
        )
        gui_handler.set_target(gui)

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui
            )
        )
        cli: CLI = CLI(cli_bundle)

        return IDECobotBundleRegistry.create_bundle(
            dependencies=IDECobotBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                streamer=streamer,
                cli=cli
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
