init 3:
    # By shifting the priority of this block, we're letting the game first load
    # in the DLC sprites and also generate the `im.Blur` versions of the sprites.
    
    layeredimage eileen:
        yanchor 0.5
        yoffset sprite_offsets['eileen']

        group bodies auto
        group eyes auto
        group faces auto
        group misc auto

    layeredimage eileen right:
        yanchor 0.5
        yoffset sprite_offsets['eileen_right']
        
        group bodies auto
        group eyes auto
        group faces auto
        group misc auto
    
    layeredimage eileen blur:
        yanchor 0.5
        yoffset sprite_offsets['eileen']
        
        group bodies auto
        group eyes auto
        group faces auto
        group misc auto

    image eileen_sepia = LayeredImageProxy(
        name="eileen", transform=Transform(matrixcolor=SepiaMatrix()))
