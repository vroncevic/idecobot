# -*- coding: UTF-8 -*-

'''
Module
    mycobot_dsl_service.py
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
    Defines concrete MyCobotDslService implementing end-to-end DSL workflows.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic_severity import MyCobotDiagnosticSeverity
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken
from idecobot.core.service.dsl.compiler.imycobot_compiler import IMyCobotCompiler
from idecobot.core.service.dsl.lexer.imycobot_lexer import IMyCobotLexer
from idecobot.core.service.dsl.linter.imycobot_linter import IMyCobotLinter
from idecobot.core.service.dsl.parser.imycobot_parser import IMyCobotParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotDslService:
    '''
        Coordinates lexing, parsing, linting, and compiling for myCobot DSL programs.

        It defines:

            :attributes:
                | _lexer - MyCobotLexer instance.
                | _parser - MyCobotParser instance.
                | _linter - MyCobotLinter instance.
                | _compiler - MyCobotCompiler instance.
            :methods:
                | __init__ - Initializes DSL components.
                | tokenize - Converts script to tokens.
                | parse - Parses script to AST.
                | lint - Evaluates AST with lint rules.
                | compile - Compiles AST to binary frames.
                | validate - End-to-end validation.
                | get_version - Returns service version string.
    '''

    _lexer: IMyCobotLexer
    _parser: IMyCobotParser
    _linter: IMyCobotLinter
    _compiler: IMyCobotCompiler

    def __init__(
        self,
        lexer: IMyCobotLexer,
        parser: IMyCobotParser,
        linter: IMyCobotLinter,
        compiler: IMyCobotCompiler
    ) -> None:
        '''
            Initializes DSL pipeline services with injected abstractions.

            :param lexer: Injected IMyCobotLexer instance.
            :param parser: Injected IMyCobotParser instance.
            :param linter: Injected IMyCobotLinter instance.
            :param compiler: Injected IMyCobotCompiler instance.
            :exceptions: None.
        '''
        self._lexer = lexer
        self._parser = parser
        self._linter = linter
        self._compiler = compiler

    def tokenize(self, source: str) -> Sequence[MyCobotToken]:
        '''
            Converts raw DSL script into lexical token sequence.

            :param source: Raw DSL source code string.
            :return: Sequence of lexical tokens.
            :exceptions:
                | ValueError: Invalid syntax or unrecognized token.
        '''
        return self._lexer.tokenize(source)

    def parse(self, source: str) -> MyCobotProgram:
        '''
            Parses script text into AST program.

            :param source: Raw DSL source code string.
            :return: Parsed MyCobotProgram AST instance.
            :exceptions:
                | ValueError: Syntax error during statement parsing.
        '''
        tokens: Sequence[MyCobotToken] = self.tokenize(source)
        raw_lines: list[str] = source.splitlines()

        return self._parser.parse(tokens, raw_lines)

    def lint(self, program: MyCobotProgram) -> Sequence[MyCobotDiagnostic]:
        '''
            Evaluates AST program against semantic rules.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of detected diagnostics.
            :exceptions: None.
        '''
        return self._linter.lint(program)

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        '''
            Translates AST program into binary protocol frames.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of compiled MyCobotFrame objects.
            :exceptions: None.
        '''
        return self._compiler.compile(program)

    def validate(self, source: str) -> tuple[MyCobotProgram | None, Sequence[MyCobotDiagnostic]]:
        '''
            End-to-end parse and lint returning AST and diagnostics.

            :param source: Raw DSL source code string.
            :return: Tuple of optional program AST and sequence of diagnostics.
            :exceptions: None.
        '''
        try:
            prog: MyCobotProgram = self.parse(source)
            diags: Sequence[MyCobotDiagnostic] = self.lint(prog)

            return prog, diags

        except ValueError as err:
            err_diag: MyCobotDiagnostic = MyCobotDiagnostic(
                line_number=1,
                severity=MyCobotDiagnosticSeverity.ERROR,
                code='ERR_SYNTAX',
                message=str(err)
            )

            return None, (err_diag,)

    def get_version(self) -> str:
        '''
            Returns service version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

