##################
# DLC Management #
##################

# This variable is meant to be altered by DLC packages, such as the "H" one.
# Packages are expected to add a string identifying them. This way, we know
# which DLC packages are present in the game.
init -999:
    define dlc_packages = []

# This variable is the setting that the users can control to state whether
# or not they want to play the adult content.
default persistent.h = True

# This flag is meant to control whether or not to show adult content
# in the current playthrough.
define h_available = ('h' in dlc_packages)
default allow_explicit = (h_available and persistent.h)

###############
# UI Settings #
###############

# These variables control the season that we want for the theming
# of the in-game UI. The default should be to let the gameplay
# change the `store` value accordingly. This can be overriden by
# the value in the `persistent` store.
#
# Possible values: 'fall', 'winter', None (don't override).
default persistent.ui_season = None
default ui_season = 'winter'

init python:
    def get_ui_season() -> str:
        if persistent.ui_season is None and ui_season is None:
            raise ValueError
        
        return persistent.ui_season or ui_season

# These variables control the season that we want for the theming
# of the notifications (cues). The default should be to let the gameplay
# change the `store.ui_season` value accordingly. This can be overriden by
# the below value in the `persistent` store.
#
# Possible values: 'fall', 'winter', None (don't override).
default persistent.cue_season = None

init python:
    def get_cue_season() -> str:
        if persistent.cue_season is None and ui_season is None:
            raise ValueError

        return persistent.cue_season or ui_season

# This variable sets whether or not to show music cues during gameplay.
default persistent.cue_music = False

# This variable sets whether or not to show sound cues during gameplay.
default persistent.cue_sfx = False

# This one sets the font to use during gameplay.
# Possible values: 'standard', 'dyslexia', 'sans'.
default persistent.font_mode = 'standard'

# This one defines whether to use High Contrast mode.
default persistent.high_contrast = False

##################
# Other Settings #
##################

# This one controls the speed of auto-forward mode.
default preferences.afm_time = 15

# This one controls whether we want to emphasize the voice audio.
default preferences.emphasize_audio = True

#########################
# Game State Management #
#########################

# This variable keeps track of the current scene's ID during gameplay.
default current_scene = None

# This variable tells us whether or not the game has been finished at least once.
default persistent.finished_story = False

# This variable is used for displaying phone messages.
# We need to keep this as a default because we don't want to lose the state of
# the phone between saves.
default phone = Phone()

##################
# Internal Logic #
##################

# This variable is used whenever we're trying to figure out if the player has
# already played through a specific part of the game. Make sure that the name
# of all of the scripting labels for the story start with this value!
define SCENE_LABEL_PREFIX = "scene_"
