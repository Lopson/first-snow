screen cue_overlay():
    python:
        for i in reversed(range(len(store._cues))):
            if store._cues[i].is_active():
                break
            store._cues.pop()

    vbox:
        xalign 1.0
        spacing 2

        for cue in store._cues:
            use expression cue.name pass (cue.is_active(), **cue.args)

screen cue(active, name, message):
    fixed:
        ysize 36
        if active:
            text message
