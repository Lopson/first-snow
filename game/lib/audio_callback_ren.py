"""renpy
init -2 python:
"""

from typing import TYPE_CHECKING, Callable
from renpy.audio import music
if TYPE_CHECKING:
    from renpy import config, persistent
    from .context_manager_ren import GameContext
    from .cue_code_ren import cue

_audio_callbacks: dict[str, list[Callable]] = {}
_audio_state: dict[str, list[Callable]] = {}
_audio_ctr: int = 0


def add_audio_callback(channel: str, cb: Callable) -> None:
    _audio_callbacks.setdefault(channel, [])
    _audio_callbacks[channel].append(cb)


def remove_audio_callback(channel: str, cb: Callable) -> None:
    _audio_callbacks[channel].remove(cb)
    if not _audio_callbacks[channel]:
        del _audio_callbacks[channel]


def run_audio_callbacks() -> None:
    global _audio_state, _audio_ctr
    _audio_ctr = (_audio_ctr + 1) % 10
    if _audio_ctr:
        return

    new_state = {c: music.get_playing(c) for c in _audio_callbacks}

    for channel, fn in new_state.items():
        if _audio_state.get(channel) == fn:
            continue
        for cb in _audio_callbacks[channel]:
            cb(fn)

    _audio_state = new_state


config.periodic_callbacks.append(run_audio_callbacks)


def friendly_name(fn: str) -> str:
    """
    As far as I can tell, this is just a backup solution
    in case a music or SFX file has no name defined for it.

    It becomes especially important for SFXs as originally,
    nobody seems to have wanted to write descriptions down
    for them.
    """
    return (fn
            # remove directory
            .rsplit('/', 1)[-1]
            # remove extension
            .rsplit('.', 1)[0]
            # remove separators
            .replace('_', ' ')
            .replace('-', ' ')
            # remove differentiatiors
            .rstrip('1234567890')
            )


def on_music(fn: str) -> None:
    if not persistent.cue_music: # pyright: ignore[reportAttributeAccessIssue]
        return
    if fn and GameContext.in_playthrough():
        name: str
        if tracks.get(fn):  # pyright: ignore[reportUndefinedVariable]
            name = tracks.get(fn).title # pyright: ignore[reportUndefinedVariable]
        else:
            name = friendly_name(fn)
        cue('icon', 4.0, which='music', txt=name)


def on_sound(fn: str) -> None:
    # TODO Use to-be-written SFX cue strings instead of friendly name.
    if not persistent.cue_sfx: # pyright: ignore[reportAttributeAccessIssue]
        return
    if fn and GameContext.in_playthrough():
        name = friendly_name(fn)
        cue('icon', 4.0, which='sfx', txt=name)


add_audio_callback('music',   on_music)
add_audio_callback('sound',   on_sound)
add_audio_callback('sound2',  on_sound)
add_audio_callback('loopsfx', on_sound)
