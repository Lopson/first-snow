layeredimage rose:
    yanchor 0.5
    yoffset sprite_offsets['rose']

    group bodies auto
    group eyes auto
    group faces auto


layeredimage rose_right:
    yanchor 0.5
    yoffset sprite_offsets['rose_right']

    group bodies auto
    group eyes auto
    group faces auto

image rose_blur = LayeredImageProxy(name="rose", transform=box_blur)
