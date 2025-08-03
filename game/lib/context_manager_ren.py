"""renpy
python early:
"""

_constant = True

from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from renpy import game, store, persistent
    from renpy.defaultstore import main_menu
    from renpy.python import NoRollback

@dataclass
class GameContext(NoRollback):
    seen_scenes: set[str] = set() # TODO We can auto-populate this based on `renpy.seen_label()`'s results.

    def scene_seen(self, scene_name: str) -> bool:
        # TODO Can we somehow turn this into a staticmethod?
        return False if scene_name not in self.seen_scenes else True

    def update_seen_scenes(self, scene: str) -> None:
        # TODO Can we somehow turn this into a staticmethod?
        if (not isinstance(scene, str) or
                scene not in store.scene_descriptions.keys()):
            raise ValueError
        
        self.seen_scenes.add(scene)
    
    @staticmethod
    def explicit_allowed() -> bool:
        """
        Tells us whether or not we can show explicit content.
        """
        
        if not store.h_available:
            return False
        return store.allow_explicit

    @staticmethod
    def get_act_title(name) -> str:
        """
        Returns the name of the given act.
        """

        # `act_titles` found in `game/definitions/acts.rpy`
        return store.act_titles.get(name, str(name))
    
    @staticmethod
    def get_scene_title(scene_id: str) -> str:
        """
        Returns the name of the given scene.
        """

        # `scene_titles` found in `game/definitions/scenes.rpy`

        # NOTE The split by underscore is there because whenever a scene
        # can have adult content, the scene is broken up into _a, _b, and
        # so forth. As such, we need to cover for that.
        return store.scene_titles.get(
            scene_id, store.scene_titles.get(scene_id.split('_', 1)[0]))

    @staticmethod
    def in_playthrough() -> bool:
        return not game.context().init_phase and not main_menu

    @classmethod
    def in_replay(cls) -> bool:
        return cls.in_playthrough() and store.oneshot

    @staticmethod
    def get_language() -> str | None:
        # TODO Once we've moved the english script away from the "en" folder,
        # this will have to be changed.
        # return _preferences.language
        return 'en'
