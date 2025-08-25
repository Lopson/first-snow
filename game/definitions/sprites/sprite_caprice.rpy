layeredimage caprice:
    yanchor 0.5
    yoffset sprite_offsets['caprice']

    group bodies auto
    group eyebrows auto
    group eyes auto
    group faces auto

image caprice_blur = LayeredImageProxy(
    name="caprice", transform=box_blur(size=10, separation=0.0))
