from __future__ import unicode_literals

from pygments.token import Token

from prompt_toolkit.enums import IncrementalSearchDirection, SEARCH_BUFFER

from .utils import token_list_len
from .processors import Processor

__all__ = (
    'DefaultPrompt',
)


class DefaultPrompt(Processor):
    """
    Default prompt. This one shows the 'arg' and reverse search like
    Bash/readline normally do.
    """
    def __init__(self, prompt='> '):
        self.prompt = prompt

    def run(self, cli, buffer, tokens):
        # Get text before cursor.
        if cli.is_searching:
            before = _get_isearch_tokens(cli)

        elif cli.input_processor.arg is not None:
            before = _get_arg_tokens(cli)

        else:
            before = [(Token.Prompt, self.prompt)]

        # Insert before buffer text.
        shift_position = token_list_len(before)

        return before + tokens, lambda i: i + shift_position

    def invalidation_hash(self, cli, buffer):
        return (
            cli.input_processor.arg,
            cli.is_searching,
            cli.buffers[SEARCH_BUFFER].text,
        )


def _get_isearch_tokens(cli):
    def before():
        if cli.search_state.direction == IncrementalSearchDirection.BACKWARD:
            text = 'reverse-i-search'
        else:
            text = 'i-search'

        return [(Token.Prompt.Search, '(%s)`' % text)]

    def text():
        return [(Token.Prompt.Search.Text, cli.buffers[SEARCH_BUFFER].text)]

    def after():
        return [(Token.Prompt.Search, '`: ')]

    return before() + text() + after()


def _get_arg_tokens(cli):
    """
    Tokens for the arg-prompt.
    """
    arg = cli.input_processor.arg

    return [
        (Token.Prompt.Arg, '(arg: '),
        (Token.Prompt.Arg.Text, str(arg)),
        (Token.Prompt.Arg, ') '),
    ]
