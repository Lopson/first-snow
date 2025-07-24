init python:
    ## Jukebox support functions.
    from dataclasses import dataclass
    from typing import Optional

    # Register channel.
    renpy.music.register_channel('jukebox', 'jukebox', False, tight=True)

    # Reload the screen when the queue became empty to update play status.
    def jukebox_empty():
        if not renpy.music.get_playing('jukebox'):
            if jukebox_empty.was_playing:
                jukebox_empty.was_playing = False
                renpy.restart_interaction()
        elif not jukebox_empty.was_playing:
            jukebox_empty.was_playing = True

    jukebox_empty.was_playing = False
    renpy.music.set_queue_empty_callback(jukebox_empty, channel='jukebox')

    def JukeboxEnter():
        return Stop('music', fadeout=1.0)

    def JukeboxLeave():
        return Stop('jukebox', fadeout=1.0)

    def jukebox_is_playing():
        return jukebox_now_playing() is not None

    def jukebox_now_playing():
        return renpy.music.get_playing('jukebox')

    def JukeboxPosition():
        return AudioPositionValue('jukebox')

    def jukebox_pos():
        return renpy.music.get_pos('jukebox')

    def JukeboxPlay(track: str = None):
        if track:
            pl = Play('jukebox', track, fadein=2.0) 
        else:
            pl = PauseAudio('jukebox', False)
        return [ Stop('music', fadeout=1.0), pl ]

    def JukeboxPause():
        return PauseAudio('jukebox', True)

    def JukeboxToggle():
        return PauseAudio('jukebox', 'toggle')

    def JukeboxStop(fadeout=None):
        return Stop('jukebox', fadeout=None)

    def JukeboxVolume():
        return Preference('jukebox volume')

    def jukebox_is_paused():
        return renpy.music.get_pause('jukebox')

    def jukebox_volume():
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

        def __hash__(self):
            return hash((self.startidx,
                self.current,
                self.curridx,
                self.previdx,
                self.nextidx))
    
    # The function that updates the jukebox's state.
    def update_jukebox_state(
            new_track: str = None,
            tracks: dict = {},
            needs_unlock: bool = False) -> JukeboxState:
        jukebox_state: JukeboxState = JukeboxState()

        for i, (track, title) in enumerate(tracks.items()):
            # Find first unlocked track to use as start track
            if (jukebox_state.startidx is None and
                    (not needs_unlock or track in persistent.played_tracks)):
                jukebox_state.startidx = i
            
            # Currently playing track?
            if new_track == track:
                jukebox_state.current = title
                jukebox_state.curridx = i
                
                # Find first unlocked previous track
                for j in reversed(range(0, jukebox_state.curridx)):
                    if (needs_unlock and
                            list(tracks.keys())[j] not in persistent.played_tracks):
                        continue
                    
                    jukebox_state.previdx = j
                    break
                else:
                    previdx = None
                
                # Find first unlocked next track
                for j in range(jukebox_state.curridx + 1, len(tracks)):
                    if (needs_unlock and
                            list(tracks.keys())[j] not in persistent.played_tracks):
                        continue
                    
                    jukebox_state.nextidx = j
                    break
                else:
                    jukebox_state.nextidx = None
                break
        
        return jukebox_state
