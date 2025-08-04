# script.rpy
# Starting point of gameplay.

# A new game has been started, initialize relevant variables.
label start:
    $ store.current_scene = None
    
    jump scene_1S1


# This label is meant to be called at the start of all scripts.
label scene_start:
    $ text_log = TextLog()
    return


# This label is meant to be called at the end of all scripts.
label scene_end:
    scene black with dissolve
    return
