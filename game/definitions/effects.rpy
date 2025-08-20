# effects.rpy
# All effect (transformation/transition) definitions are stored here.

python early:
    @renpy.atl_warper
    def eyewarp(x):
        return x**1.33

    @renpy.atl_warper
    def easeout_subtle(t):
        return pow(t, 1.25)

    @renpy.atl_warper
    def easein_subtle(t):
        return 1 - easeout_subtle(1 - t)

    @renpy.atl_warper
    def ease_subtle(t):
        if t < .5:
            return easeout_subtle(t * 2.0) / 2.0
        else:
            return 1 - easeout_subtle((1 - t)* 2.0) / 2.0


# Transistion definitions
define smoothDissolve = Dissolve(0.5, old_widget=None, new_widget=None, alpha=True)
define fastDissolve = Dissolve(0.5, old_widet=None, new_widget=None, alpha=True)
define midDissolve = Dissolve(1.5, old_widget=None, new_widget=None, alpha=True)
define midlongDissolve = Dissolve(2.0, old_widget=None, new_widget=None, alpha=True)
define longDissolve = Dissolve(3.0, old_widget=None, new_widget=None, alpha=True)
define verylongDissolve = Dissolve(5.0, old_widget=None, new_widget=None, alpha=True)
# hmm
define thelongestDissolve = Dissolve(7.0, old_widget=None, new_widget=None, alpha=True)
define thefinalDissolve = Dissolve(20.0, old_widget=None, new_widget=None, alpha=True)
define fadeInOut = Fade(1.0, 0, 1.0)
define menuFade = Fade(2,0,1, color="#f0f0f0")
define inkfade = ImageDissolve(Tile("vfx/inkfade.webp"), 2.8, 15)
define inkfade2 = ImageDissolve(Tile("vfx/inkfade.webp"), 2.2, 15)
define flash = Fade(0.6, 0.0, 1.0, color="#fff")
define circlewipe = ImageDissolve("vfx/circlewipe.webp", 2.0, 8)
define eye_open = ImageDissolve("vfx/eye.webp", .8, ramplen=128, reverse=False, time_warp=eyewarp)
define eye_shut = ImageDissolve("vfx/eye.webp", .8, ramplen=128, reverse=True, time_warp=eyewarp)


# Sprite position definitions
init -2 python:
    leftoffscreen = Position(xpos=0.0,xanchor=1.0,ypos=1.0,yanchor=1.0)
    leftedge = Position(xpos=0.05,xanchor=0.5,ypos=1.0,yanchor=1.0)
    leftside = Position(xpos=0.15,xanchor=0.5,ypos=1.0,yanchor=1.0)
    left2 = Position(xpos=0.225,xanchor=0.5,ypos=1.0,yanchor=1.0)
    leftish = Position(xpos=0.3,xanchor=0.5,ypos=1.0,yanchor=1.0)
    centerleft = Position(xpos=0.35,xanchor=0.5,ypos=1.0,yanchor=1.0)
    offcenterleft = Position(xpos=0.45,xanchor=0.5,ypos=1.0,yanchor=1.0)
    center = Position(xpos=0.5,xanchor=0.5,ypos=1.0,yanchor=1.0)
    offcenterright = Position(xpos=0.55,xanchor=0.5,ypos=1.0,yanchor=1.0)
    centerright = Position(xpos=0.65,xanchor=0.5,ypos=1.0,yanchor=1.0)
    rightish = Position(xpos=0.7,xanchor=0.5,ypos=1.0,yanchor=1.0)
    right2 = Position(xpos=0.775,xanchor=0.5,ypos=1.0,yanchor=1.0)
    rightside = Position(xpos=0.85,xanchor=0.5,ypos=1.0,yanchor=1.0)
    rightedge = Position(xpos=0.95,xanchor=0.5,ypos=1.0,yanchor=1.0)
    rightoffscreen = Position(xpos=1.0,xanchor=0.0,ypos=1.0,yanchor=1.0)
    
transform null:
    pass

# Center
transform center:
    xanchor 0.5
    xpos 0.5 yalign 1.0

# Close
transform closeleft:
    xanchor 0.5
    xpos .30 yalign 1.0

transform closeright:
    xanchor 0.5
    xpos .70 yalign 1.0

# Near
transform midleft:
    xanchor 0.5
    xpos .15 yalign 1.0

transform midright:
    xanchor 0.5
    xpos .85 yalign 1.0

# Far
transform farleft:
    xanchor 0.5
    xpos .07 yalign 1.0

transform farright:
    xanchor 0.5
    xpos .93 yalign 1.0

# Whereever you are
transform exleft:
    xanchor 0.5
    xpos -0.10 yalign 1.0

transform exright:
    xanchor 0.5
    xpos 1.10 yalign 1.0


# Effects
transform delayed(delay):
    alpha 0
    time delay
    alpha 1

init -2:
    transform showrepeat(first, firstdur, then, thendur):
        first
        time firstdur
        block:
            then
            time thendur
            repeat

transform moveto(t, x):
    subpixel True
    ease t xalign x

transform movetop(t, x):
    subpixel True
    ease t xpos x

transform trotate(alpha):
    subpixel True
    rotate alpha

transform tprotate(alpha):
    subpixel True
    rotate alpha
    rotate_pad False

transform transparent(a):
    alpha a

transform tdissolve(length):
    alpha 0.0
    linear length alpha 1.0

transform tddissolve(length, delay):
    alpha 0.0
    pause delay
    linear length alpha 1.0

transform fadein(speed):
    alpha 0.0
    linear speed alpha 1.0

transform mirror:
    xzoom -1.0

transform jflip(scale=1.0, wait=0.0, duration=0.2):
    time wait
    xzoom scale
    easein duration xzoom 0.0
    easeout duration xzoom -scale

transform jflipto(new, scale=1.0, wait=0.0, duration=0.2):
    time wait
    xzoom scale
    easein duration xzoom 0.0
    new
    easeout duration xzoom -scale

transform jcollapse(scale=1.0, wait=0.0, duration=0.2):
    time wait
    xzoom scale
    easein duration xzoom 0.0
    easeout duration xzoom scale

transform jcollapseto(new, scale=1.0, wait=0.0, duration=0.2):
    time wait
    xzoom scale
    easein duration xzoom 0.0
    new
    easeout duration xzoom scale

transform shaking:
    linear 0.08 xoffset 1
    linear 0.08 xoffset -1
    repeat
    
transform shaking2:
    linear 0.08 xoffset 1
    linear 0.08 xoffset -1
    linear 0.08 xoffset 1
    linear 0.08 xoffset -1
    linear 0.08 xoffset 0
    
transform bounce:
    pause .15
    yoffset 0
    easein .15 yoffset -18
    easeout .175 yoffset 0
    easein .15 yoffset -8
    easeout .175 yoffset 0
    yoffset 0
    
transform stretch:
    yoffset 0
    easein .25 yoffset -15
    easeout .2 yoffset 0
    easein .25 yoffset -5
    easeout .2 yoffset 0
    yoffset 0
    
transform nod:
    ease 0.5 yoffset 5
    ease 0.5 yoffset -5
    ease 0.2 yoffset 0

transform nod2:
    ease 0.5 xoffset 5
    ease 0.5 xoffset -5
    ease 0.2 xoffset 0
    
transform nod2_repeat:
    ease 0.5 xoffset 5
    ease 0.5 xoffset -5
    ease 0.2 xoffset 0
    repeat

transform box_blur:
    shader "shaders.box_blur"
    mesh True

    u_size 5
    u_separation 2.5


image snow light starting = LightSnow(prefill=False)
image snow light = LightSnow(prefill=True)
image snow light switch = LightSnow(prefill=True)
image snow sepia = LightSnowSepia(prefill=True)

# Image effects
init python:
    def vblur(name: str, img):
        """
        Returns a displayable with the blur effect applied to it.

        @param name: The name of the displayable that's to be manipulated. This
        is here so that we can specifically apply a different blur value to
        Eileen's sprites.
        @param img: The displayable that we want blurred.
        @return: A blurred displayable.
        """
        
        # fixes the scary eyes
        if name.startswith('eileen'):
            radius = 2.2
        else:
            radius = 5.0
        return im.Blur(img, radius)
