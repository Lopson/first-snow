layeredimage eve:
    yanchor 0.5
    yoffset sprite_offsets['eve']

    group bodies auto
    group eyes auto
    group faces auto

image eve_blur = LayeredImageProxy(name="eve", transform=box_blur)
