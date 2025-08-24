# init.rpy
# Initialization code for the game, and for when a new game is started.

init -1 python hide:
    # fast skip is so fast that with our directing it crashes Ren'Py lol
    config.keymap['fast_skip'] = []

init python hide:
    # Cheater cheater cheateerrrrr
    if renpy.loadable('secret-unlock.txt'):
        achievement.grant('h')

    # Patch version management
    if (persistent.patch_version or 1) < config.patch_version:
        # TODO Remove unnecessary variables from previous patch version.
        store.patch_updated = True
    else:
        store.patch_updated = False
    persistent.patch_version = config.patch_version

    # Register appropriate extra channels.
    renpy.music.register_channel(name='sound2', mixer='sfx', loop=False, tight=True)
    renpy.music.register_channel(name='loopsfx', mixer='sfx', loop=True, tight=True)
    renpy.music.register_channel(name='ambiance', mixer='ambiance', loop=True, tight=True)
    renpy.music.register_channel(name='ambiance2', mixer='ambiance', loop=True, tight=True)
    renpy.music.register_channel(name='jukebox', mixer='jukebox', loop=False, tight=True)

    # Sync progress.
    achievement.sync()


label splashscreen:
    scene black
    # needs to have an interaction before accessing renderer info
    pause 0

    # Determine if we're running a software renderer.
    if renpy.get_renderer_info()['renderer'] == 'sw':
        scene misc heres a nickel kid get yourself a better computer
        $ renpy.transition(dissolve)
        $ renpy.pause()
        scene black with dissolve
        $ renpy.quit()

    # Show a nice intro video.
    $ renpy.movie_cutscene("images/vfx/intro.ogv")
    $ renpy.transition(dissolve)
    return
