"""renpy
init -2 python:
"""

from typing import TYPE_CHECKING, Callable
from renpy.audio import music
if TYPE_CHECKING:
    from renpy import config

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
