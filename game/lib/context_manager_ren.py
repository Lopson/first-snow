"""renpy
init -26 python:
"""

from dataclasses import dataclass
from typing import TypeAlias, TYPE_CHECKING
from renpy.audio.music import play
from renpy.exports.contextexports import get_game_runtime
from renpy.exports.persistentexports import seen_label
from renpy.exports.scriptexports import get_all_labels
from renpy import game
if TYPE_CHECKING:
    from renpy import store
    from renpy.defaultstore import main_menu
    from renpy.python import NoRollback

SaveFileInfo: TypeAlias = dict[str, int | float | str | list[int]]

@dataclass
class GameContext(NoRollback):
    @staticmethod
    def scenes_seen() -> list[str]:
        result: list[str] = []
        scene_labels: list[str] = [
            i for i in get_all_labels() if i.startswith(store.SCENE_LABEL_PREFIX)
        ]

        for scene_id in store.scene_titles:
            # NOTE A scene may have been broken up into multiple sub-scenes
            # due to the adult content.
            specific_scene_labels: list[str] = [
                i for i in scene_labels if i.startswith("scene_{}".format(scene_id))
            ]

            for scene_label in specific_scene_labels:
                if seen_label(scene_label):
                    result.append(scene_id)
                    break
        
        return result
    
    @classmethod
    def scene_seen(cls, scene_id: str) -> bool:
        return scene_id in cls.scenes_seen()

    @classmethod
    def acts_seen(cls) -> set[int]:
        result: set[int] = set()
        scenes_seen: list[str] = cls.scenes_seen()
        
        for scene_seen in scenes_seen:
            result.add(int(scene_seen.split(sep="S")[0]))
        
        return result

    @classmethod
    def act_seen(cls, act_id: int) -> bool:
        return act_id in cls.acts_seen()
    
    @staticmethod
    def explicit_allowed() -> bool:
        """
        Tells us whether or not we can show explicit content.
        """
        
        if not store.h_available:
            return False
        return store.allow_explicit

    @staticmethod
    def get_act_title(act_id: int) -> str:
        """
        Returns the name of the given act.
        """

        # `act_titles` found in `game/definitions/acts.rpy`
        return store.act_titles.get(act_id, str(act_id))
    
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
        return cls.in_playthrough() and store._in_replay

    @staticmethod
    def get_language() -> str | None:
        # TODO Once we've moved the english script away from the "en" folder,
        # this will have to be changed.
        # return _preferences.language
        return 'en'

    @staticmethod
    def store_scene(info: SaveFileInfo) -> None:
        """
        Adds the current scene and total game runtime to the save file.
        """
        
        info['scene'] = store.current_scene
        # TODO Do we even need this? This is already stored in "_game_runtime".
        info['playtime'] = get_game_runtime()
    
    @staticmethod
    def store_patch_version(info: SaveFileInfo) -> None:
        """
        Adds the current patch version number to the save file.
        """

        info['patch_version'] = config.patch_version # pyright: ignore[reportAttributeAccessIssue]
    
    @staticmethod
    def replay_end_callback() -> None:
        """
        Actions to take after replay ends.
        """
        play(get_menu_theme(), if_changed=True) # pyright: ignore[reportUndefinedVariable]


"""renpy
init -25 python hide:
"""

from renpy import config

# Add save callbacks.
config.save_json_callbacks.append(GameContext.store_scene)
config.save_json_callbacks.append(GameContext.store_patch_version)
config.after_replay_callback = GameContext.replay_end_callback
