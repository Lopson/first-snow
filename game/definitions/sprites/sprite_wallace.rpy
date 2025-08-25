layeredimage wallace:
    yanchor 0.5
    yoffset sprite_offsets['wallace']

    group bodies auto
    group eyebrows auto
    group eyes auto
    group faces auto


layeredimage wallace_right:
    yanchor 0.5
    yoffset sprite_offsets['wallace_right']

    group bodies auto
    group eyebrows auto
    group eyes auto
    group faces auto

image wallace_blur = LayeredImageProxy(
    name="wallace", transform=box_blur(size=10, separation=0.0))
