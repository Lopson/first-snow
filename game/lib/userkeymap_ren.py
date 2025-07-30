# User-defined keymap functionality.
# Copyright (C) 2014-2016 Shiz.
# Tested on Ren'Py v6.99.8.
# Released under the terms of the WTFPL; see http://sam.zoy.org/wtfpl/COPYING for details.
#
# Usage: Loop over ukm_event_order in a screen for a list of events to bind to.
#  Skip None entries, they are there for adding spacing if you want to.
#  For every event entry, loop over ukm_get_bindings(event) for a list of current bindings for that event as (binding, name, joy) tuples.
#
#  ukm_add_binding(event, binding, joy) is function that will add the given keymap binding.
#  AddUserKeyBinding(event, binding, joy) is the equivalent screen action.
#  ukm_remove_binding(event, binding, joy) is a function that will remove the given keymap binding.
#  RemoveUserKeyBinding(event, binding, joy) is the equivalent screen action.
#  `event` is an event name as in ukm_event_order, `binding` and `joy` are the variables stored by KeyBindingGrabBehaviour (see below).
#
#  To add a key binding, add KeyBindingGrabBehaviour('target_var', exclude_displayables=[...])
#  to a dedicated screen where the user can input their desired keybind.
#  The exclude_displayables parameter should be a list of displayable IDs that the code should ignore when grabbing input.
#  This should usually be the confirm and cancel buttons at the least, so the user can exit the screen properly.
#  The last pressed key binding will be stored in the store variable whose name is given as the first argument.
#  For instance, if the string 'key_binding' is given, the binding will be stored in store.key_binding.
#  The key binding stored is a tuple of (binding, name, joy). `binding` and `joy` are the parameters
#  that should be passed to ukm_add_binding()/AddUserKeyBinding().
#
#  Trimmed-down example from Twofold code:
#
# screen preferences_keymap:
#     on "hide" action Hide('preferences_kemap_add')
#     on "replaced" action Hide('preferences_keymap_add')
#
#     ...
#
#                 for event in ukm_event_order:
#                     if event is None:
#                         null height 25
#                     else:
#                         label ukm_event_descriptions[event]:
#                             ...
#
#                         hbox:
#                             ...
#
#                             for binding, name, joy in ukm_get_bindings(event):
#                                 label name:
#                                     ...
#                                 imagebutton:
#                                     ...
#                                     action RemoveUserKeyBinding(event, binding, joy)
#
#                             imagebutton:
#                                 ...
#                                 action Show('preferences_keymap_add', dissolve, event)
#
# screen preferences_keymap_add(event):
#     python:
#         if not hasattr(store, '_keymap_captured_key'):
#             store._keymap_captured_key = (None, None, None)
#
#         binding, name, joy = store._keymap_captured_key
#         if not name:
#             name = '(nothing)'
#
#     frame id "preferences_keymap_add_frame":
#         ...
#
#         add KeyBindingGrabBehaviour('_keymap_captured_key', exclude_displayables=['keymap_add_ok', 'keymap_add_cancel'])
#
#         text "Please press the keys or buttons you want to bind.":
#             ...
#
#         text name:
#             ...
#
#         imagebutton id "keymap_add_ok":
#             ...
#             action [ AddUserKeyBinding(event, binding, joy), Hide('preferences_keymap_add', dissolve) ]
#
#         imagebutton id "keymap_add_cancel":
#             ...
#            action Hide('preferences_keymap_add', dissolve)
#

"""renpy
init 1 python:
"""

from collections import OrderedDict
from sys import platform
import pygame_sdl2 as pygame  # pyright: ignore[reportMissingImports]
from renpy.game import persistent
from renpy import config, store
from renpy.minstore import _
from renpy.ui import Action
from renpy.display.core import IgnoreEvent, EVENTNAME
from renpy.display.behavior import map_event, clear_keymap_cache
from renpy.exports.displayexports import restart_interaction, get_image_bounds
# _keymap_list is impossible to import as it resides in 00keymap.rpy


def ukm_restore_bindings() -> None:
    if not persistent._ukm_default_keymap:
        persistent._ukm_default_keymap = {
            k: list(v) for k, v in config.keymap.items()}

    if persistent._ukm_user_keymap:
        config.keymap = {
            k: _keymap_list(v) for k, v in persistent._ukm_user_keymap.items()} # pyright: ignore[reportUndefinedVariable]

    if not persistent._ukm_default_joymap:
        persistent._ukm_default_joymap = {
            k: list(v) for k, v in config.pad_bindings.items()}
    if persistent._ukm_user_joymap:
        config.pad_bindings = {
            k: _keymap_list(v) for k, v in persistent._ukm_user_joymap.items()} # pyright: ignore[reportUndefinedVariable]


def ukm_save_bindings() -> None:
    persistent._ukm_user_keymap = {
        k: list(v) for k, v in config.keymap.items()}
    persistent._ukm_user_joymap = {
        k: list(v) for k, v in config.pad_bindings.items()}


def ukm_reset_bindings() -> None:
    config.keymap = {
        k: _keymap_list(v) for k, v in persistent._ukm_user_keymap.items()} # pyright: ignore[reportUndefinedVariable]
    config.pad_bindings = {
        k: _keymap_list(v) for k, v in persistent._ukm_user_joymap.items()} # pyright: ignore[reportUndefinedVariable]


# Event types.
# https://github.com/pygame/pygame/blob/main/buildconfig/stubs/pygame/constants.pyi
UKM_MOUSE_EVENT_TYPES: set[int] = {
    pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL}
UKM_KEYBOARD_EVENT_TYPES: set[int] = {pygame.KEYDOWN, pygame.KEYUP}
UKM_CONTROLLER_EVENT_TYPES: set[int] = {EVENTNAME}
UKM_INPUT_EVENT_TYPES: set[int] = UKM_MOUSE_EVENT_TYPES | UKM_KEYBOARD_EVENT_TYPES | UKM_CONTROLLER_EVENT_TYPES
UKM_KEYBOARD_MODIFIERS: OrderedDict[str, int] = OrderedDict([
    ('meta', pygame.KMOD_META),
    ('ctrl', pygame.KMOD_CTRL),
    ('alt', pygame.KMOD_ALT),
    ('shift', pygame.KMOD_SHIFT)
])

# Human-readable keymap descriptions.
ukm_event_descriptions: dict[str, str] = dict(
    rollback=_('Roll back text'),
    screenshot=_('Take screenshot'),
    toggle_fullscreen=_('Toggle fullscreen'),
    game_menu=_('Menu'),
    text_log=_('Text log'),
    hide_windows=_('Hide UI'),
    quit=_('Quit'),
    iconify=_('Minimize'),
    help=_('Help'),

    rollforward=_('Roll forward text'),
    dismiss=_('Advance text'),
    dismiss_hard_pause=_('Force advance text'),
    toggle_afm=_('Toggle auto-advance'),

    skip=_('Skip text'),
    toggle_skip=_('Toggle skipping text'),

    save_delete=_('Delete save file'),

    developer=_('Developer menu'),
    launch_editor=_('Launch editor'),
    choose_renderer=_('Renderer choice'),
    reload_game=_('Reload game'),
    inspector=_('Style inspector'),

    focus_up=_('Up'),
    focus_down=_('Down'),
    focus_left=_('Left'),
    focus_right=_('Right')
)

# Keymap order. None indicates vertical spacing.
ukm_event_order: list[str | None] = [
    'dismiss',
    'rollback',
    'rollforward',
    'toggle_afm',
    'skip',
    'toggle_skip',
    None,

    'hide_windows',
    'screenshot',
    'game_menu',
    'text_log',
    'help',
    'toggle_fullscreen',
    'iconify',
    'quit',
    None,

    'focus_left',
    'focus_right',
    'focus_up',
    'focus_down'
]
if config.developer:
    ukm_event_order.extend([
        None,

        'developer',
        'reload_game',
        'inspector',
        'launch_editor'
    ])

# Name for keysyms.
ukm_keysym_names: dict[str, str] = {
    'EXCLAIM': u'!',
    'QUOTE': u"'",
    'QUOTEDBL': u'"',
    'HASH': u'#',
    'DOLLAR': u'$',
    'AMPERSAND': u'&',
    'LEFTPAREN': u'(',
    'RIGHTPAREN': u')',
    'ASTERISK': u'*',
    'PLUS': u'+',
    'COMMA': u',',
    'MINUS': u'-',
    'PERIOD': u'.',
    'SLASH': u'/',
    'COLON': u':',
    'SEMICOLON': u';',
    'LESS': u'<',
    'EQUALS': u'=',
    'GREATER': u'>',
    'QUESTION': u'?',
    'AT': u'@',
    'LEFTBRACKET': u'[',
    'BACKSLASH': u'\\',
    'RIGHTBRACKET': u']',
    'CARET': u'^',
    'UNDERSCORE': u'_',
    'BACKQUOTE': u'`',
    'UP': _('Up'),
    'LEFT': _('Left'),
    'RIGHT': _('Right'),
    'DOWN': _('Down'),
    'NUMLOCK': _('Num lock'),
    'CAPSLOCK': _('Caps lock'),
    'SCROLLOCK': _('Scroll lock'),
    'LSHIFT': u'Shift',
    'RSHIFT': u'Right shift',
    'LCTRL': _('Ctrl'),
    'RCTRL': _('Right ctrl'),
    'LALT': _('Alt'),
    'RALT': _('Right alt'),
    'LMETA': _('Ctrl') if platform != 'darwin' else _('Cmd'),
    'RMETA': _('Right ctrl') if platform != 'darwin' else _('Cmd'),
    'LGUI': _('Menu') if platform != 'darwin' else _('Cmd'),
    'RGUI': _('Right menu') if platform != 'darwin' else _('Cmd'),
    'LSUPER': _('Win'),
    'RSUPER': _('Win'),
    'EURO': u'€',
    'RETURN': 'Enter',
    'PAGEUP': 'Page up',
    'PAGEDOWN': 'Page down',
    'ESCAPE': 'Esc',
    'DELETE': 'Del'
}

ukm_mouse_button_names: dict[str, str] = {
    '1': 'Left click',
    '2': 'Middle click',
    '3': 'Right click',
    '4': 'Scroll up',
    '5': 'Scroll down'
}

ukm_position_names: dict[str, str] = {
    'pos':  'up',
    'neg':  'down',
    'None': 'neutral'
}

ukm_keysym_values: dict[str, int] = {
    val: name for name, val in pygame.__dict__.items() if name.startswith('K_')}


def ukm_binding_to_friendly(name: str) -> str | None:
    keyname: list[str] = []
    suffix: str = ''

    # Modifier keys.
    if name.lower().startswith('repeat_'):
        name = name[len('repeat_'):]
        suffix += ' (held down)'
    if name.lower().startswith('noshift_'):
        name = name[len('noshift_'):]

    while any(name.lower().startswith(meta + '_') for
              meta in ('super', 'meta', 'ctrl', 'alt', 'shift')):
        meta, name = name.split('_', 1)
        keyname.append(ukm_keysym_names['L' + meta.upper()])

    # Joystick keys.
    if name.startswith('pad_'):
        _, interface, position = name.split('_', 2)

        if position in ('pos', 'neg', 'None'):
            interface = interface\
                .replace('left', 'left stick ')\
                .replace('right', 'right stick ')
            name = '{} {}'.format(interface.capitalize(),
                                  ukm_position_names[position])
            name = name.replace('x down', 'left')\
                .replace('x up', 'right')\
                .replace('y down', 'up')\
                .replace('y up', 'down')
        else:
            interface = interface\
                .replace('left', 'left ')\
                .replace('right', 'right ')\
                .replace('dp', 'd-pad ')\
                .replace('guide', 'home')
            name = '{}-button'.format(interface.capitalize())

        keyname.append(name)
        return ' + '.join(keyname)

    # Keyboard key name mangling.
    if name.startswith('K_'):
        # K_ENTER, K_ESCAPE...
        name = name[2:]
    if name.startswith('KP'):
        # KP0, KP_DIVIDE...
        name = name[2:].lstrip('_')
        suffix += ' (keypad)'
    if name.startswith('AC_'):
        # AC_BACK, AC_HOME...
        name = name[3:]
        suffix += ' (media)'

    if not name:
        return None

    if len(name) == 1:
        # a, A, 0...
        keyname.append(name.upper() + suffix)
    elif name.startswith('mousedown') or name.startswith('mouseup'):
        # Mouse names.
        _, button = name.split('_', 1)
        keyname.append(ukm_mouse_button_names.get(
            button, 'Mouse button #{}'.format(button)))
    elif name.startswith('F'):
        # F1, F2...
        keyname.append(name + suffix)
    elif name in ukm_keysym_names:
        # Known keyboard symbols.
        keyname.append(ukm_keysym_names[name] + suffix)
    else:
        # Fallback, simply capitalize the raw name.
        keyname.append(name.capitalize() + suffix)

    return ' + '.join(keyname)


def ukm_extract_binding(event: pygame.event.Event) -> tuple[bool, str | None] | None:
    if event.type in UKM_MOUSE_EVENT_TYPES:
        if event.type != pygame.MOUSEBUTTONUP:
            return (False, None)
        return (False, 'mouseup_{}'.format(event.button))
    elif event.type in UKM_KEYBOARD_EVENT_TYPES:
        if event.type != pygame.KEYDOWN:
            return (False, None)

        base: int | None = ukm_keysym_values.get(event.key)
        mods = []
        for name, mod in UKM_KEYBOARD_MODIFIERS.items():
            if event.mod & mod:
                mods.append(name)

        if base and mods:
            return (False, '_'.join(mods) + '_' + str(base))
        elif base:
            return (False, str(base))
        elif mods:
            return (False, '_'.join(mods))
        else:
            return (False, None)
    elif event.type in UKM_CONTROLLER_EVENT_TYPES:
        return (True, str(event.controller))


def ukm_get_bindings(command: str) -> list[tuple[str, str | None, bool]]:
    syms: list[tuple[str, str | None, bool]] = [
        (sym, ukm_binding_to_friendly(sym), False) for
        sym in config.keymap.get(command, [])]
    
    sym: str
    commands: list[str]
    for sym, commands in config.pad_bindings.items():
        if command in commands:
            syms.append((sym, ukm_binding_to_friendly(sym), True))
    return syms


def ukm_add_binding(event: str, binding: str, joy: bool) -> None:
    if joy:
        config.pad_bindings.setdefault(binding, [])
        config.pad_bindings[binding].append(event)
    else:
        config.keymap.setdefault(event, [])
        config.keymap[event].append(binding)

    ukm_save_bindings()
    clear_keymap_cache()
    restart_interaction()


def ukm_remove_binding(event: str, binding: str, joy: bool) -> None:
    if joy:
        if binding in config.pad_bindings and event in config.pad_bindings[binding]:
            config.pad_bindings[binding].remove(event)
    else:
        if event in config.keymap and binding in config.keymap[event]:
            config.keymap[event].remove(binding)

    ukm_save_bindings()
    clear_keymap_cache()
    restart_interaction()


def ukm_reset_all_bindings() -> None:
    ukm_reset_bindings()
    ukm_save_bindings()
    clear_keymap_cache()
    restart_interaction()



class KeyBindingGrabBehaviour(Null): # pyright: ignore[reportUndefinedVariable]
    def __init__(self,
                 target: str,
                 excludes: list[str]=[],
                 exclude_displayables: list[str]=[],
                 **kwargs) -> None:
        super(KeyBindingGrabBehaviour, self).__init__(**kwargs)
        self.target: str = target
        self.excludes: list[str] = excludes
        self.exclude_displayables: list[str] = exclude_displayables

    def event(self, ev: pygame.event.Event, x: int, y: int, st: str) -> None:
        # NOTE I believe the "st" argument stands for style.

        # Check event types.
        if ev.type not in UKM_INPUT_EVENT_TYPES:
            return

        # Check excluded events.
        for exclude in self.excludes:
            if map_event(ev, exclude):
                return

        # Check for a mouse event in excludes displayables.
        if ev.type in UKM_MOUSE_EVENT_TYPES:
            evx: int
            evy: int
            evx, evy = ev.pos

            for displayable in self.excludes:
                if (result := get_image_bounds(displayable)) is not None:
                    width: int
                    height: int
                    x, y, width, height = result
                    # Within bounds?
                    if (evx >= x and evy >= y and evx <= x + width and evy <= y + height):
                        return

        # Store event and tell Ren'Py to ignore it.
        if (result := ukm_extract_binding(ev)) is not None:
            joy, sym = result
            if sym is not None:
                setattr(store, self.target,
                        (sym, ukm_binding_to_friendly(sym), joy))

        restart_interaction()
        raise IgnoreEvent()


class AddUserKeyBinding(object):
    def __init__(self, command: str, binding: str, joy: bool) -> None:
        self.command: str = command
        self.binding: str = binding
        self.joy: bool = joy

    def __call__(self) -> None:
        if self.binding:
            ukm_add_binding(self.command, self.binding, self.joy)


class RemoveUserKeyBinding(object):
    def __init__(self, command: str, binding: str, joy: bool) -> None:
        self.command: str = command
        self.binding: str = binding
        self.joy: bool = joy

    def __call__(self) -> None:
        ukm_remove_binding(self.command, self.binding, self.joy)


class ResetUserKeyBindings(Action):
    def __call__(self) -> None:
        ukm_reset_all_bindings()


ukm_restore_bindings()
