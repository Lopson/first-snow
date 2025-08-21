layeredimage millie:
    yanchor 0.5
    yoffset sprite_offsets['millie']

    group bodies auto
    group eyebrows auto
    group eyes auto
    group misc auto
    group mouths auto


layeredimage millie_right:
    yanchor 0.5
    yoffset sprite_offsets['millie_right']

    group bodies auto
    group eyebrows auto
    group eyes auto
    group misc auto
    group mouths auto

image millie_blur = LayeredImageProxy(name="millie", transform=box_blur)
