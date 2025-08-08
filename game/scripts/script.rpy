# script.rpy
# Starting point of gameplay.

# A new game has been started, initialize relevant variables.
label start:
    $ current_scene = None
    $ text_log = None
    $ phone = Phone()
    
    jump scene_1S1


# This label is meant to be called at the start of all scripts.
label scene_start(scene_id):
    $ text_log = TextLog()
    $ current_scene = scene_id
    return


# This label is meant to be called at the end of all scripts.
label scene_end:
    # TODO Is this scene statement really necessary?
    scene black with dissolve
    $ renpy.end_replay()
    return
