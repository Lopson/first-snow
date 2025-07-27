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

python early:
    import collections

    def doublespeak_parse(lexer):
        leftchar = lexer.simple_expression()
        rightchar = lexer.simple_expression()

        leftmsg = eval(lexer.simple_expression())
        if lexer.eol():
            rightmsg = leftmsg
        else:
            rightmsg = eval(lexer.simple_expression())

        if not lexer.eol():
            renpy.error('unexpected leftover data')

        return { 'chars': [leftchar, rightchar], 'messages': [leftmsg, rightmsg] }

    def doublespeak(info):
        info = multispeak_process(info)
        longest = sorted(info['messages'], key=len, reverse=True)[0]

        renpy.shown_window()
        renpy.show_screen('say', double_speak=True, who=info['evaluated_chars'], what=info['messages'])

        ui.saybehavior(afm=longest)
        result = ui.interact(roll_forward=renpy.roll_forward_info(), type='say')
        renpy.checkpoint(result)

        for (name, char), message in zip(info['evaluated_chars'].items(), info['messages']):
            char.do_done(name, message)

    def multispeak_process(info):
        # Get proper character names.
        chars = collections.OrderedDict()
        for name in info['chars']:
            char = eval(name)

            if getattr(char, 'dynamic', False):
                name = eval(char.name)
            else:
                name = char.name
            chars[name] = char
        info['evaluated_chars'] = chars

        # Adjust messages properly.
        messages = []
        for (name, char), message in zip(info['evaluated_chars'].items(), info['messages']):
            message = char.what_prefix + message + char.what_suffix
            messages.append(message)
        info['messages'] = messages

        return info

    def multispeak_predict(info):
        return []

    def multispeak_lint(info):
        for char in info['chars']:
            try:
                eval(char)
            except:
                renpy.error('unknown character {0}'.format(char))

    def multispeak_next(info):
        return None

    renpy.statements.register('doublespeak', parse=doublespeak_parse, execute=doublespeak, predict=multispeak_predict, lint=multispeak_lint, next=multispeak_next)
