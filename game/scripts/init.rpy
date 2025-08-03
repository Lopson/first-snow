# init.rpy
# Global script initialization.

label scene_init:
    python:
        all_languages = []
        store.ui_season = 'winter'

label scene_start:
    $ text_log = TextLog()
    return

label scene_end:
    scene black with dissolve
    return
