layeredimage eileen:
    yanchor 0.5
    yoffset sprite_offsets['eileen']

    group bodies auto:
        attribute naked_crossed:
            ConditionSwitch(
                "h_available", "dlc/h/sprites/eileen/bodies/eileen_bodies_naked_crossed.webp",
                "True", "null"
            )
        attribute naked_fists:
            ConditionSwitch (
                "h_available", "dlc/h/images/sprites/eileen/bodies/eileen_bodies_naked_fists.webp",
                "True", "null"
            )
        attribute naked_onhip:
            ConditionSwitch (
                "h_available", "dlc/h/images/sprites/eileen/bodies/eileen_bodies_naked_onhip.webp",
                "True", "null"
            )
    group eyes auto
    group faces auto
    group misc auto

layeredimage eileen right:
    yanchor 0.5
    yoffset sprite_offsets['eileen_right']
    
    group bodies auto:
        attribute naked_crossed:
            ConditionSwitch(
                "h_available", "dlc/h/sprites/eileen/bodies/eileen_right_bodies_naked_crossed.webp",
                "True", "null"
            )
        attribute naked_fists:
            ConditionSwitch (
                "h_available", "dlc/h/sprites/eileen/bodies/eileen_right_bodies_naked_fists.webp",
                "True", "null"
            )
        attribute naked_onhip:
            ConditionSwitch (
                "h_available", "dlc/h/sprites/eileen/bodies/eileen_right_bodies_naked_onhip.webp",
                "True", "null"
            )
    group eyes auto
    group faces auto
    group misc auto

image eileen_sepia = LayeredImageProxy(
    name="eileen", transform=Transform(matrixcolor=SepiaMatrix()))

image eileen_blur = LayeredImageProxy(name="eileen", transform=box_blur)
