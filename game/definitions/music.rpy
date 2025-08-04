init -1 python:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from renpy import persistent

    def get_menu_theme() -> str:
        return 'music/snow-eileen.ogg' if persistent.finished_story else 'music/snow.ogg'

init python:
    from collections import namedtuple
    from enum import StrEnum

    class MusicType(StrEnum):
        MAIN = "main"
        EVENT = "event"
        EXCLUDE = "exclude"

    TrackDetails = namedtuple("TrackDetails", ["title", "type"])

define fadeout_music_room = 1.0
define fadein_music_room = 2.0

define standard_music_room = MusicRoom(
    channel='jukebox', fadeout=fadeout_music_room,
    fadein=fadein_music_room, single_track=True)

define event_music_room = MusicRoom(
    channel='jukebox', fadeout=fadeout_music_room,
    fadein=fadein_music_room, single_track=True)

define tracks = {
    'music/snow.ogg': TrackDetails(__('Snowy City'), MusicType.MAIN),
    'music/art_club_a.ogg': TrackDetails(__('Watercolors'), MusicType.MAIN),
    'music/relaxing.ogg': TrackDetails(__('Winding Down'), MusicType.MAIN),
    'music/caprice_default_m.ogg': TrackDetails(__('Cute Salute'), MusicType.MAIN),
    'music/anxiety_2_m.ogg': TrackDetails(__('So You Do Have a Name'), MusicType.MAIN),
    'music/energetic.ogg': TrackDetails(__('The Usual Excitement'), MusicType.MAIN),
    'music/caprice_ringtone.ogg': TrackDetails(__('Ringtone (Caprice)'), MusicType.EVENT),
    'music/whimsical_faster_m.ogg': TrackDetails(__('Comfortable Silence'), MusicType.MAIN),
    'music/conflict.ogg': TrackDetails(__('Bitter Medicine'), MusicType.MAIN),
    'music/romance_2_m.ogg': TrackDetails(__('Butterflies'), MusicType.EVENT),
    'music/millie_2.ogg': TrackDetails(__('Boundless Worlds'), MusicType.EVENT),
    'music/questioning.ogg': TrackDetails(__('Sketchy Skills'), MusicType.MAIN),
    'music/zoo_4_m2.ogg': TrackDetails(__('Unexpected Comfort'), MusicType.EVENT),
    'music/touching.ogg': TrackDetails(__('Wonderful Warmth'), MusicType.EVENT),
    'music/snow_4_m.ogg': TrackDetails(__('Snow Circles'), MusicType.EVENT),
    'music/night_2.ogg': TrackDetails(__('Warm-Hearted World'), MusicType.MAIN),
    'music/dozy_comfy.ogg': TrackDetails(__('Pick-Me-Up'), MusicType.MAIN),
    'music/more_sad_m.ogg': TrackDetails(__('Left Behind'), MusicType.EVENT),
    'music/eve_3_m.ogg': TrackDetails(__('Sibling Scuffles'), MusicType.EVENT),
    'music/eileen_5_m.ogg': TrackDetails(__('Mixed Messages'), MusicType.MAIN),
    'music/diner_2_m2.ogg': TrackDetails(__('Prost!'), MusicType.EVENT),
    'music/painter.ogg': TrackDetails(__('Did You Paint All These?'), MusicType.EVENT),
    'music/ringtone.ogg': TrackDetails(__('Ringtone'), MusicType.EVENT),
    'music/credits.ogg': TrackDetails(__('Snowmelt'), MusicType.EVENT),
    'music/snow-eileen.ogg': TrackDetails(__('Our Snowy City'), MusicType.EVENT),
    'music/night_2_r2.ogg': TrackDetails(__('Warm-Hearted World'), MusicType.EXCLUDE)
}

init python:
    # Add all of the tracks to the music room.
    for track in (i for i in tracks if tracks[i].type == MusicType.MAIN):
        standard_music_room.add(track, always_unlocked=True)

    for track in (i for i in tracks if tracks[i].type == MusicType.EVENT):
        event_music_room.add(track)


    def get_current_mr_track_index(music_room: MusicRoom) -> int:
        if music_room.last_playing is None:
            return -1

        idx: int
        try:
            idx = music_room.playlist.index(music_room.last_playing)
        except ValueError:
            idx = -1
        
        return idx


    def get_current_mr_track_file(music_room: MusicRoom) -> str:
        idx: int = get_current_mr_track_index(music_room)

        if idx >= 0:
            return music_room.playlist[idx]
        return ""


    def is_current_mr_playing(music_room: MusicRoom) -> bool:
        if get_current_mr_track_index(music_room) < 0:
            return False
        
        if not renpy.music.is_playing(music_room.channel):
            return False
        return True
