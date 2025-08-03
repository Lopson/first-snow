init python:
    # TODO Try to break these back into regular images or SpriteManager objects.
    # Only handle this once you've gotten the game back to stable post-RABBL removal.

    animation_from_folder(
        'menu_newgame', 'ui/side/menu_new', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_savegame', 'ui/side/menu_save', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_savegame_back', 'ui/side/menu_back1', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_loadgame', 'ui/side/menu_load', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_loadgame_back', 'ui/side/menu_back2', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_options', 'ui/side/menu_options', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_options_back', 'ui/side/menu_back3', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_extras', 'ui/side/menu_extras', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_extras_back', 'ui/side/menu_back4', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_mainmenu', 'ui/side/menu_main', wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_quit_normal', 'ui/side/menu_quit', fps=18, loop_frames=1,
        wrapper=ResettableDisplayable)
    
    animation_from_folder(
        'menu_quit_reverse', 'ui/side/menu_quit', reverse=True, fps=18,
        loop_frames=1, wrapper=ResettableDisplayable)
