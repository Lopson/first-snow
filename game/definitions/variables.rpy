# This object contains data about the player's overall progress.
default game_context = GameContext()

# These variables control the season that we want for the theming
# of the in-game UI. The default should be to let the gameplay
# change the `store` value accordingly. This can be overriden by
# the value in the `persistent` store.
#
# Possible values: 'fall', 'winter', None (don't override).
default persistent.ui_season = None
default store.ui_season = 'winter'

init python:
    def get_ui_season() -> str:
        if persistent.ui_season is None and store.ui_season is None:
            raise ValueError
        
        return persistent.ui_season or store.ui_season

# These variables control the season that we want for the theming
# of the notifications (cues). The default should be to let the gameplay
# change the `store.ui_season` value accordingly. This can be overriden by
# the below value in the `persistent` store.
#
# Possible values: 'fall', 'winter', None (don't override).
default persistent.cue_season = None

init python:
    def get_cue_season() -> str:
        if persistent.cue_season is None and store.ui_season is None:
            raise ValueError

        return persistent.cue_season or store.ui_season
