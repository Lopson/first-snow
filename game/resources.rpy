# resources.rpy
# Contains all resources: sprites, backgrounds, characters...

define DEFAULT_BLUR_VALUE = 5.0
define EILEEN_BLUR_VALUE = 2.2

init:
    # Images and effects.
    image white = Solid("#ffffff")
    image creme = Solid("#fffbf4")
    image shadow = Solid("#000")
 
    image cg title = "ui/main/bg.webp"

    image cue bg = Composite(
        (config.screen_width, 29),
        (0, 3), "ui/hud/cue/bg.webp",
        (226, 3), "#2b3038"
    )

    # Images for which to create a sepia version.
    define sepia_images = [
        'bg downtown park',
        'bg colorado town hd',
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

    # Images for which to create a blurred version with a custom blur value.
    define blur_images = [
        ('bg aptallison outside', 1.0),
        ('bg aptallison outside night', 2.0),
        ('bg aptallison livingroom', 2.0),
        ('bg aptallison livingroom', 5.0),
        ('bg aptallison road dusk', 4.0),
        ('bg apteileen livingroom', 2.0),
        ('bg apteileen livingroom hd', 2.0),
        ('bg apteileen livingroom hd', 5.0),
        ('bg apteileen livingroom messy', 2.0),
        ('bg apteileen livingroom messy norabbit', 2.0),
        ('bg apteileen livingroom messy hd', 4.0),
        ('bg buildingmisc generichall', 2.0),
        ('bg buildingmisc library', 2.0),
        ('bg buildingmisc library hd', 2.0),
        ('bg buildingart art dusk', 2.0),
        ('bg buildingart art dusk siren', 1.0),
        ('bg buildingart art dusk womanwip', 1.0),
        ('bg buildingart art dusk bustsketch', 2.0),
        ('bg buildingart hallway2f dusk hd', 2.0),
        ('bg buildingunion outside snow', 2.0),
        ('bg cafe inside', 2.0),
        ('bg cafe inside hd', 2.0),
        ('bg campus outskirts snow', 2.0),
        ('bg colorado house ext', 4.0),
        ('bg colorado house livingroom fire', 2.0),
        ('bg colorado house livingroom night', 4.0),
        ('bg colorado house guestbedroom', 4.0),
        ('bg colorado colorado hiking loop', 2.0),
        ('bg colorado hiking2', 4.0),
        ('bg colorado town hd', 4.0),
        ('bg colorado park', 2.0),
        ('bg colorado town', 2.0),
        ('bg downtown city', 3.0),
        ('bg downtown park', 3.0),
        ('bg downtown pizzeria', 2.0),
        ('bg downtown square night', 2.0),
        ('bg misc zoo', 2.0),
        ('bg misc zoo hd', 2.0),
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


init python:
    # Dynamically load sprites and backgrounds not found in the default
    # `images` folder. In Ren'Py 8.5 and above, this will no longer be
    # necessary as you can just alter the variable config.image_directories.

    for package in [None] + store.dlc_packages:
        if package:
            pfx = 'dlc/' + package + '/'
        else:
            pfx = ''
        
        if pfx:
            config.images_directory = 'dlc/' + package + '/images'
            _scan_images_directory()
            config.images_directory = 'images'


init 2 python:
    # NOTE Init level set to 2 to allow DLCs to add images to some of the lists
    # defined in this file.
        
    # This for loop cycle is here to ensure retrocompatibility with the
    # rest of the game's code base. Images were being defined with two specific
    # alignment transforms; now that we're having Ren'Py define these images on
    # its own, we still need to apply that transform. This code does just that.
    #
    # FWIW the only image that wouldn't play well with not having these
    # alignments was "cg act3 familydinner 1hd.jpg" to my knowledge.
    for image_name in [i for i in renpy.list_images() if i.startswith(("cg", "bg"))]:
        renpy.image(
            image_name,
            At(
                get_base_image(image_name),
                Transform(xalign=0.5, yalign=0.5)
            )
        )
    
    # We're creating a blurred variant for every single background image. For
    # retrocompatibility reasons, we're doing this to all of the backgrounds,
    # but in reality we only really need to do this for those that show up in
    # the scripting with the attribute "blur".
    for image_name in [i for i in renpy.list_images() if i.startswith("bg")]:
        renpy.image(
            image_name + " blur",
            At(
                im.Blur(get_base_image(image_name), DEFAULT_BLUR_VALUE),
                Transform(xalign=0.5, yalign=0.5)
            )
        )

    # Generate all of the sepia variants of the images we've selected. Note how
    # this original piece of code doesn't create these images with align
    # properties like the rest of the CGs and BGs.
    for image_name in sepia_images:
        renpy.image(
            image_name + ' sepia',
            At(
                get_base_image(image_name),
                Transform(xalign=0.5, yalign=0.5, matrixcolor=SepiaMatrix())
            )
        )

    # Generate all of the custom blur variants of the images we've selected.
    # Note how this original piece of code doesn't create these images with
    # align properties like the rest of the CGs and BGs.
    for image_name, amount in blur_images:
        renpy.image(
            image_name + ' blurred{}'.format(int(amount)),
            At(
                im.Blur(get_base_image(image_name), amount),
                Transform(xalign=0.5, yalign=0.5)
            )
        )
