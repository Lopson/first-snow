"""renpy
python early:
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from renpy import game
    from renpy.defaultstore import main_menu

@dataclass
class GameContext:
    seen_scenes: set[str] = set() # TODO We can auto-populate this based on `renpy.seen_label()`'s results.
    current_scene: str | None = None
    oneshot: bool = False
    allow_explicit: bool = True

    def scene_seen(self, scene_name: str) -> bool:
        # TODO Can we somehow turn this into a staticmethod?
        return False if scene_name not in self.seen_scenes else True

    def update_seen_scenes(self, scene: str) -> None:
        if not isinstance(scene, str) or scene not in scene_descriptions.keys(): # pyright: ignore[reportUndefinedVariable]
            raise ValueError
        
        self.seen_scenes.add(scene)

    def get_act_title(self, name) -> str:
        return act_titles.get(name, str(name)) # pyright: ignore[reportUndefinedVariable]
    
    def get_title(self, name) -> str:
        return scene_titles.get(name, scene_titles.get(name.split('_', 1)[0])) # pyright: ignore[reportUndefinedVariable]

    @staticmethod
    def in_playthrough() -> bool:
        return not game.context().init_phase and not main_menu

    def in_replay(self) -> bool:
        return self.in_playthrough() and self.oneshot
