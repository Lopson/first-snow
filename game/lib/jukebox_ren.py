"""renpy
init python:
"""

## Jukebox support functions.

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, TypeVar
from renpy.audio import music
from renpy.exports.displayexports import restart_interaction
if TYPE_CHECKING:
    from renpy import game
    from renpy import persistent

was_playing: bool = False

# Register channel.
music.register_channel('jukebox', 'jukebox', False, tight=True)

# Reload the screen when the queue became empty to update play status.
def jukebox_empty() -> None:
    global was_playing
    
    if not music.get_playing('jukebox'):
        if was_playing:
            was_playing = False
            restart_interaction()
    elif not was_playing:
        was_playing = True

music.set_queue_empty_callback(jukebox_empty, channel='jukebox')

def JukeboxEnter() -> Stop:
    return Stop('music', fadeout=1.0)

def JukeboxLeave() -> Stop:
    return Stop('jukebox', fadeout=1.0)

def jukebox_is_playing() -> bool:
    return jukebox_now_playing() is not None

def jukebox_now_playing() -> None:
    return music.get_playing('jukebox')

def JukeboxPosition() -> AudioPositionValue:
    return AudioPositionValue('jukebox')

def jukebox_pos() -> int:
    return music.get_pos('jukebox') # pyright: ignore[reportReturnType]

def JukeboxPlay(track: str | None = None) -> Stop:
    if track:
        pl = Play('jukebox', track, fadein=2.0) 
    else:
        pl = PauseAudio('jukebox', False)
    return [ Stop('music', fadeout=1.0), pl ]

def JukeboxPause() -> PauseAudio:
    return PauseAudio('jukebox', True)

def JukeboxToggle() -> PauseAudio:
    return PauseAudio('jukebox', 'toggle') # pyright: ignore[reportUndefinedVariable]

def JukeboxStop(fadeout=None) -> Stop:
    return Stop('jukebox', fadeout=None)

def JukeboxVolume() -> Preference:
    return Preference('jukebox volume') # pyright: ignore[reportUndefinedVariable]

def jukebox_is_paused() -> bool:
    return music.get_pause('jukebox')

def jukebox_volume() -> float:
    return game.preferences.get_volume('jukebox')

# Object that's meant to be used by the Jukebox screen
# to keep track of how to operate/display properly.
@dataclass
class JukeboxState:
    startidx: Optional[int] = None
    current: Optional[str] = None
    curridx: Optional[int] = None
    previdx: Optional[int] = None
    nextidx: Optional[int] = None

    def __hash__(self) -> int:
        return hash((self.startidx,
            self.current,
            self.curridx,
            self.previdx,
            self.nextidx))

# The function that updates the jukebox's state.
def update_jukebox_state(
        new_track: str | None = None,
        tracks: dict = {},
        needs_unlock: bool = False) -> JukeboxState:
    jukebox_state: JukeboxState = JukeboxState()

    for i, (track, title) in enumerate(tracks.items()):
        # Find first unlocked track to use as start track
        if (jukebox_state.startidx is None and
                (not needs_unlock or track in persistent.played_tracks)): # pyright: ignore[reportAttributeAccessIssue]
            jukebox_state.startidx = i
        
        # Currently playing track?
        if new_track == track:
            jukebox_state.current = title
            jukebox_state.curridx = i
            
            # Find first unlocked previous track
            for j in reversed(range(0, jukebox_state.curridx)):
                if (needs_unlock and
                        list(tracks.keys())[j] not in persistent.played_tracks): # pyright: ignore[reportAttributeAccessIssue]
                    continue
                
                jukebox_state.previdx = j
                break
            
            # Find first unlocked next track
            for j in range(jukebox_state.curridx + 1, len(tracks)):
                if (needs_unlock and
                        list(tracks.keys())[j] not in persistent.played_tracks): # pyright: ignore[reportAttributeAccessIssue]
                    continue
                
                jukebox_state.nextidx = j
                break
            else:
                jukebox_state.nextidx = None
            break
    
    return jukebox_state
