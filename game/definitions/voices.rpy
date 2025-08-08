init python:
    from collections import namedtuple

    VoiceDetails = namedtuple(
        "VoiceDetails", ["tag", "character_name", "va_name", "color"])

define voices = [
    VoiceDetails(
        'allison',   __('Allison Merlo'),    __('Elizabeth Quedenfeld'), '#1c2831'),
    VoiceDetails(
        'eileen',    __('Eileen Turner'),    __('Kira Buckland'),        '#9a9065'),
    VoiceDetails(
        'rose',      __('Rose Garcia'),      __('Nola Klop'),            '#c7633b'),
    VoiceDetails(
        'wallace',   __('Wallace Moore'),    __('Steven Kelly'),         '#b2678a'),
    VoiceDetails(
        'caprice',   __('Caprice Shiften'),  __('Lisa Reimold'),         '#839093'),
    VoiceDetails(
        'millie',    __('Millie Clarke'),    __('Jill Harris'),          '#925254'),
    VoiceDetails(
        'hayley',    __('Hayley Curah'),     __('Elissa Park'),          '#cc9351'),
    VoiceDetails(
        'eve',       __('Eve Turner'),       __('Aimee Smith'),          '#9a9065'),
    VoiceDetails(
        'elizabeth', __('Elizabeth Turner'), __('Abigail Turner'),       '#9a9065'),
    VoiceDetails(
        'andrew',    __('Andrew Turner'),    __('Bradley Gareth'),       '#5b4741'),
]

init python:
    def play_vo_test(voice: str, sample: str) -> None:
        act = PlayCharacterVoice(voice, sample, selected=True)
        if not act.get_selected():
            renpy.run(act)

    def stop_vo_test() -> None:
        renpy.music.stop('voice', fadeout=1.0)

    def sustain_vo_test(
            e: ExtendableEvent,
            voice: str,
            amount: float,
            volume: float=None) -> None:
        if e.has_ended():
            e.interval = amount
            e.start()
        else:
            e.extend(amount)
        renpy.run(SetCharacterVolume(voice, volume))
        renpy.music.set_volume(volume, channel='voice')
        renpy.restart_interaction()
