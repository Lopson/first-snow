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


screen cue_icon(active, which, txt):
    python:
        season = get_cue_season()
        text_color = {
            'fall':   '#352114',
            'winter': '#424351'
        }[season]
        outline_color = {
            'fall':   '#f9f8d1',
            'winter': '#faf6e7'
        }[season]
        icon = "ui/hud/cue/icon-{}-{}.webp".format(which, season)
        bg = Frame("ui/hud/cue/bg-{}.webp".format(season), tile=True, padding=(0, 0), margin=(0, 0))

    frame:
        background "cue bg"
        ysize 32
        xpos 1.0
        xanchor 1.0
        margin (0, 0)
        padding (0, 0)

        if active:
            hbox:
                xminimum 200

                add icon

                label txt:
                    background bg
                    text_size 20
                    xminimum 160
                    ymaximum 32
                    text_color text_color
                    text_outlines [(2, outline_color, 0, 0)]
                    text_yoffset 3
                    margin (0, 0)
                    padding (0, 0, 5, 0)
        else:
            null width 0
