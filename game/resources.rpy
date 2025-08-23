# resources.rpy
# Contains all resources: sprites, backgrounds, characters...

# Dynamically load sprites and backgrounds.
init python:
    for package in [None] + store.dlc_packages:
        if package:
            pfx = 'dlc/' + package + '/'
        else:
            pfx = ''

        # TODO Remove the Eileen DLC sprite explicit definition in her
        # layered image object once you've gone ahead and implemented this whole
        # thing using just `_scan_images_directory()` and `config.images_directory`.
        # Once we get there, I'm guessing the game with automatically populate the
        # layered image with those components?

        # TODO
        define_images(pfx + 'bgs', ['bg'], xalign=0.5, yalign=0.5, variants={'blur': vblur})
        
        if pfx:
            config.images_directory = 'dlc/' + package + '/images/cgs'
            _scan_images_directory()
            config.images_directory = 'images'
            # define_images(pfx + 'cgs', ['cg'], xalign=0.5, yalign=0.5)

        # TODO
        define_images(pfx + 'vfx', ['misc'])
        # TODO
        define_images(pfx + 'vfx/cutins', ['cutin'])
        # TODO
        define_images(pfx + 'vfx/title', ['title'])
        # TODO
        define_images(pfx + 'vfx/notes', ['note'])
    
    # NOTE This for loop cycle is here to ensure retrocompatibility with the
    # rest of the game's code base. These images that are not automatically
    # discovered by Ren'Py were being defined with two specific alignment
    # transforms; now that we're having Ren'Py define these images on its own,
    # we still need to apply that transform. This code does just that.
    #
    # FWIW the only image that wouldn't play well with not having these
    # alignments was "cg act3 familydinner 1hd.jpg" to my knowledge.
    for image_name in [i for i in renpy.list_images() if i.startswith("cg")]:
        renpy.image(image_name, Transform(
            get_base_image(image_name), xalign=0.5, yalign=0.5))
        

# Sepia and blur filters
init python:
    sepia_images = [
        'bg downtown park',
        'bg colorado town HD',
        'bg colorado house ext',
        'bg colorado hiking2',
        'cg act2 kiss after',
        'cg act3 swings foreground',
        'cg act3 swings2',
        'cg act1 eileenpainting',
        'misc rendered eileen first meeting',
        'misc rendered eileen painting flashback',
        'misc rendered eileen physical flashback',
        'misc rendered eileen hiking flashback',
        'misc rendered eileen leaving colorado',
    ]

    blur_images = [
        ('bg aptallison outside', 1.0),
        ('bg aptallison outside night', 2.0),
        ('bg aptallison livingroom', 2.0),
        ('bg aptallison livingroom', 5.0),
        ('bg aptallison road dusk', 4.0),
        ('bg apteileen livingroom', 2.0),
        ('bg apteileen livingroom HD', 2.0),
        ('bg apteileen livingroom HD', 5.0),
        ('bg apteileen livingroom messy', 2.0),
        ('bg apteileen livingroom messy norabbit', 2.0),
        ('bg apteileen livingroom messy HD', 4.0),
        ('bg buildingmisc generichall', 2.0),
        ('bg buildingmisc library', 2.0),
        ('bg buildingmisc library HD', 2.0),
        ('bg buildingart art dusk', 2.0),
        ('bg buildingart art dusk siren', 1.0),
        ('bg buildingart art dusk womanwip', 1.0),
        ('bg buildingart art dusk bustsketch', 2.0),
        ('bg buildingart hallway2f dusk HD', 2.0),
        ('bg buildingunion outside snow', 2.0),
        ('bg cafe inside', 2.0),
        ('bg cafe inside HD', 2.0),
        ('bg campus outskirts snow', 2.0),
        ('bg colorado house ext', 4.0),
        ('bg colorado house livingroom fire', 2.0),
        ('bg colorado house livingroom night', 4.0),
        ('bg colorado house guestbedroom', 4.0),
        ('bg colorado colorado hiking loop', 2.0),
        ('bg colorado hiking2', 4.0),
        ('bg colorado town HD', 4.0),
        ('bg colorado park', 2.0),
        ('bg colorado town', 2.0),
        ('bg downtown city', 3.0),
        ('bg downtown park', 3.0),
        ('bg downtown pizzeria', 2.0),
        ('bg downtown square night', 2.0),
        ('bg misc zoo', 2.0),
        ('bg misc zoo HD', 2.0),
        ('cg act1 eileenpainting', 4.0),
        ('cg act1 eileenpainting eileen', 1.0),
        ('cg act2 balconychat talk 4', 2.0),
        ('cg act2 photo', 2.0),
        ('cg act2 nudepainting', 4.0),
        ('cg act3 roadtrip 1', 4.0),
        ('cg act3 snowmen', 4.0),
        ('cg act3 swings', 2.0),
        ('cg act3 swings foreground', 0.8),
        ('cg act3 hug end', 5.0)
    ]

init 2 python:
    # different init level to allow DLC to add images in init level 1
    
    for img in sepia_images:
        renpy.image(img + ' sepia', Transform(get_base_image(img), matrixcolor=SepiaMatrix()))

    for img, amount in blur_images:
        renpy.image(img + ' blurred{}'.format(int(amount)), im.Blur(get_base_image(img), amount))

init:
    # Images and effects.
    image white = Solid("#ffffff")
    image creme = Solid("#fffbf4")
    image shadow = Solid("#000")
    image cg title = "ui/main/bg.webp"
