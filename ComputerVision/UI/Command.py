import os
import time

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.interface import AbortAction

import click

from fuzzyfinder import fuzzyfinder

from .FileSystem import Basefilepath

from pygments.lexer import RegexLexer
from pygments.lexer import bygroups
from pygments.lexer import include
from pygments.lexer import words

from pygments.style import Style
from pygments.token import *
from pygments.styles.fruity import FruityStyle

class Filepath(Basefilepath):
    def __init__(self):
        super(Filepath, self).__init__()

    def setToolbar(self):
        return self.filepath.split(os.path.split(self.systempath)[0])[-1]

class CVLexer(RegexLexer):
    # TODO
    name = 'CV'
    aliases = ['cv']
    filenames = ['*.cv']

    tokens = {
        'root': [
            ('\s+', Text),
            ('[0-9]+', Number),
            (r'\w+', Name),
        ],
    }

class CommandLineStyle(Style):
    styles = {
        # User
        Token:'#ffffff',
        # Prompt
        Token.Host:'#ffffff',
        Token.Path:'#ffffff',
        Token.Pound:'#ffffff',
        # Toolbar
        Token.Toolbar:'#ffffff bg:#333333',
        # Lexer
        Token.Name:'italic',
    }
    styles.update(FruityStyle.styles)

class CVCompleter(Completer):
    def __init__(self):
        super(CVCompleter, self).__init__()
        self.CVKeywords = [
            'new',
            ]
        
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, self.CVKeywords)
        for match in matches:
            yield Completion(match, start_position=-len(word_before_cursor))

class CommandLine(object):
    def __init__(self):
        super(CommandLine, self).__init__()
        self.num = os.system('clear')
        # init
        self.initCommand()

    def get_prompt_tokens(self, cli):
        return [
            (Token.Host, 'CV > '),
            (Token.Path, 'In [%d]'%(self.num)),
            (Token.Pound, ' -> '),
        ]

    def get_bottom_toolbar_tokens(self, cli):
        filepath = Filepath()
        return [(Token.Toolbar, '%>% Path: ' + filepath.setToolbar() + ' %>% ' + time.strftime("%Y-%m-%d %H:%M:%S"))]

    def get_title(self):
        return 'PyCV'

    def continuation_tokens(self, cli, width):
        return [(Token, ' ' * (width - 5) + '.' * 4 + ' ')]

    def initCommand(self):
        print("CV 1.0.0(default, Oct 12 2017)")
        print("Type 'info' for more information")
        print("PyCV 1.0.0")
        while True:
            try:
                self.num += 1
                user_input = prompt(
                    history=FileHistory('history.txt'),
                    enable_history_search=True,
                    auto_suggest=AutoSuggestFromHistory(),
                    lexer=CVLexer,
                    completer=CVCompleter(),
                    get_prompt_tokens=self.get_prompt_tokens,
                    get_bottom_toolbar_tokens=self.get_bottom_toolbar_tokens,
                    style=CommandLineStyle,
                    refresh_interval=1,
                    get_title=self.get_title,
                    on_abort=AbortAction.RETRY,
                    # multiline=True,
                    # get_continuation_tokens=self.continuation_tokens,
                    # mouse_support=True,
                    )
                click.secho('CV > Out[%d] -> '%(self.num), nl=False, fg='white')
                click.echo(user_input)
                # click.echo_via_pager(user_input)
            except EOFError:
                break