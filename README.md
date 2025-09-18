# Twofold: First Snow

![HACKERWOMAN](https://github.com/salty-salty-studios/first-snow/blob/main/sourcecode.png?raw=true)

## Overview

This is the source code for First Snow. It is released in the hope people can learn from it, make translations, and modify it to their needs and wishes (with the license conditions in mind).

## Requirements

* A relatively modern PC (anything made in the former half of the 10's will do fine), running either:
  * Windows XP+ (but please do upgrade to a more modern Windows)
  * OS X 10.7+
  * Linux with glibc or glibc-compatible libc and X11
* Ren'Py 7.4.11
* Some creativity (optional!)

## Working with the script

First Snow uses a semi-custom script system called RABBL. This allowed the developers to efficiently manage choice structures, if First Snow had any, and at some point before Ren'Py had built-in translation support, translations.

The game story is handled by the master script file in `game/script/script.rpy`. This file contains the entry point for RABBL and guides the general script flow. It tells the engine what scenes to perform, what choices should be made and how the results should be handled, centrally.

RABBL introduces the perform statement to perform a scene. Essentially, ignoring all the tiny extras RABBL gives us, this calls the label `scene_<name>_<currentlanguage>`. Likewise, there is also the choice statement to perform a choice. This, again, gives us some tiny extras, but also fixes the choice so it can't be made again when rolling back. It calls c`hoice_<name>_<currentlanguage> `to display the choice, and relies that said label returns a numeric value indicating what choice was made.

RABBL and, as a result, First Snow do not support Ren'Py's built-in translation system because they predate it. However, RABBL is internationalization-friendly: to translate, all you need to do is copy game/scripts/en to your target language (e.g. `game/scripts/fr`), rename all labels from `_en` to `_fr`, and add the new language to `all_languages` in `game/script/init.rpy`. You then can start translating! Translation requires at least a tiny amount of familiarity with Ren'Py's script format.

All new scenes must be added to the `scenes` variable in `game/script/init.rpy` in order to be registered with the scene replay system and have their title shown in the pause menu. They also need an entry in `game/script/sceneshots` if they aren't set to hidden in the scene replay system.

All new characters must be registered using the `characters` variable in `game/script/init.rpy` and `character_names` and `character_tags` (if applicable) variables in `game/script/<language>/init.rpy`. You don't have to define characters manually: just adding them here will initialize them.

All UI strings are registered in `game/script/<language>/init.rpy` for translation.

For language-specific images, please use the folder `game/vfx/<language>`. Create it if it doesn't exist.

## Working with assets

Assets are automatically defined from the folders: see `game/resources.rpy` for the exact rules. Currently, they are as follows:

* All images from `game/sprites` are defined using a custom sprite composition system: for every character, there's subfolders for every layer. The system then combines all possible combinations with an image name according to the used layers. For instance, `eileen indoors_onhip disbelief smile` consists of `game/sprites/eileen/bodies/indoors_onhip.webp`, `game/sprites/eileen/eyes/disbelief.webp` and `game/sprites/eileen/faces/smile.webp`. Layer folders starting with a `_` are optional.
* All images from `game/sprites-static` get defined as their base/folder name: `game/sprites-static/caprice/smile.png` becomes `caprice smile` and `game/sprites-static/allison/smile_eyesclosed.png` becomes `allison smile eyesclosed`. They also get adjusted vertically according to the sprite_offsets variable, defined in `game/script/init.rpy`.
* All images from `game/bgs` get defined with a `bg` prefix: `game/bgs/apartment/bathroom.png` becomes `bg apartment bathroom`.
* All images from `game/cgs` get defined with a `cg` prefix: `game/cgs/allie_intro.png` becomes `cg allie intro`.
* All images from `game/vfx` get defined with a `misc` prefix: `game/vfx/phone.png` becomes `misc phone`.

All music tracks must be added to the tracks variable in `game/script/<language>/init.rpy` in order to be registered in the jukebox and have their title shown in the pause menu.

## Working with the code

First Snow's code is managed using the [git](http://git-scm.com/) source code control system. A primer on git is available [here](http://git-scm.com/documentation).

All hacks and additions to Ren'Py are stored in the `game/lib` folder. Try to make game functionality as non-specific to First Snow as possible, and store it there. Then the game code can make use of it.

## Building distributions

Internally, First Snow distributions are built using [Drone](http://drone.io/). The exact build instructions are documented in [.drone.yml](./.drone.yml). There's three kinds of distributions built from every release:

* Regular installers for direct downloads. The source files for the installers are located in `installer/win` (Windows, [NSIS 3.0](http://nsis.sourceforge.net/)), `installer/mac` (macOS) and `installer/appimage` (Linux, [AppImage](https://appimage.org/)).
* Steam. The build metadata files are located in `installer/steam`.
* Itch.io. The build metadata is fully contained in `.drone.yml`.

## Support

This release comes without any support, warranty or guarantee that your PC won't be set on fire. However, if you have any questions, you can drop by on [our Discord](https://discord.gg/rVR6TFp), open an issue here on GitHub, or hit us up [on Twitter](https://twitter.com/saltyx2studios).
