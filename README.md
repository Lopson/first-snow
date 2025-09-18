# Twofold: First Snow

![HACKERWOMAN](https://github.com/salty-salty-studios/first-snow/blob/main/sourcecode.png?raw=true)

## Overview

This is a fork of the original source code of First Snow. The purpose of this fork is twofold:

* To make the game compatible with Ren'Py SDK 8.4.1.
* To make future maintenance work on this code base easier.

To achieve this dual purpose, a significant chunk of the code base has been modified. By code base, I mean internal game logic as well as some modifications to the presentation logic of the gameplay scripts. Many of the artistic resources have also been reorganized or removed. Finally, all of the installer logic has been removed as that's outside of the scope of this fork.

## Compliance

* This fork is a derivative work of First Snow.
* This is not an official release of First Snow by Salty Salty Studios.

I've done my best to comply with the license laid out in the original code base. If you think I've handled this part incorrectly, please open an Issue in this repository and I'll do my best to address it promptly.

## Requirements

* A PC running either:
  * Windows 10 or later
  * OS X 10.10+
  * Ubuntu 20.04 or later, the Steam "soldier" runtime, or a similar Linux distribution
* Ren'Py 8.4.1

## (New way of) working with the script

The original code base of this game relied on a custom Ren'Py "add-on" called RABBL. According to the original `README`:

> \[RABBL\] allowed the developers to efficiently manage choice structures, if First Snow had any, and at some point before Ren'Py had built-in translation support, translations.

Seeing as Ren'Py now natively supports translations and that RABBL was rather impenetrable for those without programming knowledge, it's been entirely removed from the code base. This means that the game's scripting now works like any other Ren'Py game.

## Working with assets

Some assets are automatically loaded by Ren'Py, some are defined manually. Backgrounds, cutscenes, sprites, and effects are loaded automatically, along with voice files. Everything else should be defined in an appropriate file within the directory `game/definitions`.

When the graphical assets are loaded, the following things are defined by the backend:

* All of the blurred versions are generated programatically using `im.Blur`. The use of this Image Manipulator is for retrocompatibility reasons. While a great amount of effort was put into trying to use custom shaders instead of this, the end result would never be close enough to the IM's output, and considering how important blurring is for this game's presentation, I unfortunately could not accept a sub-par substitute.
* All of the animations are constructed by the Python function `animation_from_folder` found in `game/lib/auto_animation_ren.py`. The code is fully documented. By giving this function a name for the animation's Displayable and the path to the folder containing all of the frames, the Displayable itself is created, which can then be invoked using the name given to the function.

Another important aspect is the way DLC graphical assets are loaded. In `game/definitions/images.rpy`, the backend leverages Ren'Py 8.4's automatic asset loading functionality (through `config.images_directory`) to deal with these.

## Working with the code

Please keep in mind this fork's scope before contributing new code! It should focus on increasing this code base's overall longevity. New features should stick to accessibility.

## Building distributions

The original repository of this game contained code to enable people to build the game and easily redistribute it. More specifically, it had code to build Windows and macOS installers, as well as Linux packages. All of this has been removed in this fork as it's outside the scope. Having said that, don't forget that Ren'Py's SDK can build distributables of games out-of-the-box!

## Support

The only support venue relevant to this project is this repository's Issues page.
