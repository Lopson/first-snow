# doublespeak.rpy
# Allow two characters to speak at once.
# (C) 2014 delta, Shiz
# Original code by delta, rewritten by Shiz for modern Ren'Py.
# Released under the terms of the WTFPL; see http://www.wtfpl.net/txt/copying/ for details.
#
# Usage:
#   doublespeak char1 char2 "What?"
#  or
#   doublespeak char1 char2 "What?" "What are you saying?"
#
# This will call your say screen with parameter 'doublespeak' set to True, and the who/what parameters
# will be a list instead of a string. You should add something like this to your say screen:
#   default doublespeak = False
# and then check if doublespeaking using
#   if doublespeak:
# and modify your UI accordingly.
#
# This file adds a custom Ren'Py statement: make sure it appears before the files in which you use the statement, filename-wise.
# You can achieve this by renaming the file to 00_doublespeak.rpy or something similar.

# TODO Replace all of this with "Multiple Character Dialogue"
# https://www.renpy.org/doc/html/multiple.html

"""renpy
python early:
"""

from typing import Optional, TypeAlias
from collections import OrderedDict
from renpy.exports.debugexports import error
from renpy.exports.displayexports import shown_window
from renpy.display.screen import show_screen
from renpy.exports.rollbackexports import checkpoint, roll_forward_info
from renpy.lexer import Lexer
from renpy.statements import register as register_statement # To comply with current documentation.
from renpy.ui import saybehavior, interact
from renpy.character import ADVCharacter

ParserResult: TypeAlias = dict[str, list[str] | OrderedDict[str, ADVCharacter]]


def doublespeak_parse(lexer: Lexer) -> ParserResult:
    leftchar: Optional[str] = lexer.simple_expression()
    rightchar: Optional[str] = lexer.simple_expression()

    leftmsg: Optional[str] = None
    rightmsg: Optional[str] = None

    tentative_leftmsg: Optional[str] = lexer.simple_expression()
    if tentative_leftmsg:
        leftmsg: Optional[str] = eval(tentative_leftmsg)

    if lexer.eol():
        rightmsg: Optional[str] = leftmsg
    else:
        tentative_rightmsg: Optional[str] = lexer.simple_expression()
        if tentative_rightmsg:
            rightmsg: Optional[str] = eval(tentative_rightmsg)

    if not lexer.eol():
        error('unexpected leftover data')

    def validate_value(value: Optional[str]) -> bool:
        if isinstance(value, str) and value is not None:
            return True
        return False
    
    if all(map(validate_value, [leftchar, rightchar, leftmsg, rightmsg])):
        return {'chars': [leftchar, rightchar], 'messages': [leftmsg, rightmsg]} # pyright: ignore[reportReturnType]
    raise ValueError


def doublespeak(info: ParserResult) -> None:
    info = multispeak_process(info)
    longest: str = sorted(info['messages'], key=len, reverse=True)[0]

    shown_window()
    show_screen(
        'say',
        double_speak=True,
        who=info['evaluated_chars'],
        what=info['messages'])

    saybehavior(afm=longest)
    result = interact(roll_forward=roll_forward_info(), type='say')
    checkpoint(result)

    if isinstance(info['evaluated_chars'], OrderedDict):
        for (name, char), message in zip(
                info['evaluated_chars'].items(), info['messages']):
            char.do_done(name, message)
    else:
        raise ValueError


def multispeak_process(info: ParserResult) -> dict:
    # Get proper character names.
    chars: OrderedDict[str, ADVCharacter] = OrderedDict()
    for name in info['chars']:
        char: ADVCharacter = eval(name)

        if getattr(char, 'dynamic', False):
            name: str = eval(char.name)
        else:
            name: str = char.name
        chars[name] = char
    info['evaluated_chars'] = chars

    # Adjust messages properly.
    messages: list[str] = []
    for (name, char), message in zip(info['evaluated_chars'].items(), info['messages']):
        message: str = char.what_prefix + message + char.what_suffix
        messages.append(message)
    info['messages'] = messages

    return info


def multispeak_predict(info) -> list:
    return []


def multispeak_lint(info) -> None:
    for char in info['chars']:
        try:
            eval(char)
        except:
            error('unknown character {0}'.format(char))


def multispeak_next(info) -> None:
    return None


register_statement(
    'doublespeak',
    parse=doublespeak_parse,
    execute=doublespeak,
    predict=multispeak_predict,
    lint=multispeak_lint,
    next=multispeak_next)
