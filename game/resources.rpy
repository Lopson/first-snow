# resources.rpy
# Contains all resources: sprites, backgrounds, characters...

# Characters.
define adv = Character(None, ctc=DynamicDisplayable(ctc), ctc_position="fixed")
define narrator = Character(None, what_style='say_thought')

# Dynamically load sprites and backgrounds.
init python:
    sprite_offsets = {
        'rose': 410,
        'rose_right': 410,
        'eileen': 380,
        'eileen_right': 380,
        'caprice': 450,
        'millie': 420,
        'millie_right': 420,
        'michael': 380,
        'eve': 300,
        'wallace': 370,
        'wallace_right': 370
    }

    for package in [None] + store.dlc_packages:
        if package:
            pfx = 'dlc/' + package + '/'
        else:
            pfx = ''

        define_dynamic_images(pfx + 'sprites', yanchor=0.5, variants={'blur': vblur})
        define_images(pfx + 'sprites-static')

        define_images(pfx + 'bgs', ['bg'], xalign=0.5, yalign=0.5, variants={'blur': vblur})
        define_images(pfx + 'cgs', ['cg'], xalign=0.5, yalign=0.5)

        define_images(pfx + 'vfx', ['misc'])
        define_images(pfx + 'vfx/cutins', ['cutin'])
        define_images(pfx + 'vfx/title', ['title'])
        define_images(pfx + 'vfx/notes', ['note'])

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

    def get_base_image(n):
        ref = ImageReference(n)
        if not ref.find_target():
            return None
        src = ref.target
        while True:
            if not isinstance(src, Transform):
                break
            src = src.child
        return src

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

# Eileen Flashback Layered Image
layeredimage eileen_sepia:
    group bodies:
        attribute indoors_crossed default:
            Transform("sprites/eileen/bodies/indoors_crossed.webp", matrixcolor=SepiaMatrix())
        attribute indoors_fists:
            Transform("sprites/eileen/bodies/indoors_fists.webp", matrixcolor=SepiaMatrix())
        attribute indoors_onhip:
            Transform("sprites/eileen/bodies/indoors_onhip.webp", matrixcolor=SepiaMatrix())
        attribute outdoors_crossed:
            Transform("sprites/eileen/bodies/outdoors_crossed.webp", matrixcolor=SepiaMatrix())
        attribute outdoors_fists:
            Transform("sprites/eileen/bodies/outdoors_fists.webp", matrixcolor=SepiaMatrix())
        attribute outdoors_onhip:
            Transform("sprites/eileen/bodies/outdoors_onhip.webp", matrixcolor=SepiaMatrix())
        attribute outdoorsnoscarf_crossed:
            Transform("sprites/eileen/bodies/outdoorsnoscarf_crossed.webp", matrixcolor=SepiaMatrix())
        attribute outdoorsnoscarf_fists:
            Transform("sprites/eileen/bodies/outdoorsnoscarf_fists.webp", matrixcolor=SepiaMatrix())
        attribute outdoorsnoscarf_onhip:
            Transform("sprites/eileen/bodies/outdoorsnoscarf_onhip.webp", matrixcolor=SepiaMatrix())
        attribute hiking_onhip:
            Transform("sprites/eileen/bodies/hiking_onhip.webp", matrixcolor=SepiaMatrix())
        attribute naked_towel:
            Transform("sprites/eileen/bodies/naked_towel.webp", matrixcolor=SepiaMatrix())
        attribute pjs_onhip:
            Transform("sprites/eileen/bodies/pjs_onhip.webp", matrixcolor=SepiaMatrix())
        attribute pjs_crossed:
            Transform("sprites/eileen/bodies/pjs_crossed.webp", matrixcolor=SepiaMatrix())

    group eyes:
        attribute normal default:
            Transform("sprites/eileen/eyes/normal.webp", matrixcolor=SepiaMatrix())
        attribute annoyed:
            Transform("sprites/eileen/eyes/annoyed.webp", matrixcolor=SepiaMatrix())
        attribute closed:
            Transform("sprites/eileen/eyes/closed.webp", matrixcolor=SepiaMatrix())
        attribute disbelief:
            Transform("sprites/eileen/eyes/disbelief.webp", matrixcolor=SepiaMatrix())
        attribute frowning:
            Transform("sprites/eileen/eyes/frowning.webp", matrixcolor=SepiaMatrix())
        attribute lookaway:
            Transform("sprites/eileen/eyes/lookaway.webp", matrixcolor=SepiaMatrix())
        attribute lookawaynarrow:
            Transform("sprites/eileen/eyes/lookawaynarrow.webp", matrixcolor=SepiaMatrix())
        attribute narrow:
            Transform("sprites/eileen/eyes/narrow.webp", matrixcolor=SepiaMatrix())
        attribute sad:
            Transform("sprites/eileen/eyes/sad.webp", matrixcolor=SepiaMatrix())

    group faces:
        attribute neutral default:
            Transform("sprites/eileen/faces/neutral.webp", matrixcolor=SepiaMatrix())
        attribute angry:
            Transform("sprites/eileen/faces/angry.webp", matrixcolor=SepiaMatrix())
        attribute frown:
            Transform("sprites/eileen/faces/frown.webp", matrixcolor=SepiaMatrix())
        attribute grumble:
            Transform("sprites/eileen/faces/grumble.webp", matrixcolor=SepiaMatrix())
        attribute open:
            Transform("sprites/eileen/faces/open.webp", matrixcolor=SepiaMatrix())
        attribute sadmouth:
            Transform("sprites/eileen/faces/sadmouth.webp", matrixcolor=SepiaMatrix())
        attribute smile:
            Transform("sprites/eileen/faces/smile.webp", matrixcolor=SepiaMatrix())
        
    group _misc:
        attribute none default:
            Transform("sprites/eileen/_misc/none.webp", matrixcolor=SepiaMatrix())
        attribute blush:
            Transform("sprites/eileen/_misc/blush.webp", matrixcolor=SepiaMatrix())
        attribute tears:
            Transform("sprites/eileen/_misc/tears.webp", matrixcolor=SepiaMatrix())
