# 00_config.rpy
# Basic Ren'Py game options.

python early:
    config.save_directory = "FirstSnow"
    config.testing = False
    config.patch_version = None
    config.save_dump = False
    config.log = None
    config.log_events = False

init -1 python hide:
    from math import ceil
    from renpy.defaultstore import main_menu
    from renpy.display.behavior import Keymap

    # Basic settings.
    config.name = "First Snow"
    config.version = "1.4.2"
    config.patch_version = 5
    config.developer = "auto"

    # Window.
    config.screen_width = 1280
    config.screen_height = 720
    config.window_title = u"First Snow"
    config.window_icon = "ui/icon.png"
    config.windows_icon = "ui/icon-win.png"
    config.default_fullscreen = False
    config.framerate = ceil(int(renpy.get_refresh_rate()))

    # Capabilities.
    config.gl_resize = True
    config.has_sound = True
    config.has_music = True
    config.has_voice = True
    config.main_menu_music = get_menu_theme()
    config.has_autosave = False
    config.has_quicksave = False

    # Misc.
    config.auto_voice = "voice/{id}.ogg"
    config.voice_filename_format = "voice/{filename}"
    config.default_text_cps = 25
    config.thumbnail_width = 193
    config.thumbnail_height = 108
    config.check_conflicting_properties = True

    # Theme.
    theme.marker(
        widget = "#003c78",
        widget_hover = "#0050a0",
        widget_text = "#c8ffff",
        widget_selected = "#ffffc8",
        disabled = "#404040",
        disabled_text = "#c8c8c8",
        label = "#ffffff",
        frame = "#6496c8",
        mm_root = "#000000",
        gm_root = "#dcebff",
        rounded_window = False
    )
    style.default.font = "ui/SetFireToTheRain.ttf"

    # Keymap.
    config.keymap['choose_renderer'] = []
    config.keymap['text_log'] = ['l']

    # History
    config.history_length = 100
    gui.history_blocked_tags = [ 'nw' ]

    def toggle_text_log():
        if not main_menu:
            ToggleScreen('text_log', dissolve)() # type: ignore

    config.underlay.append(Keymap(text_log=toggle_text_log))

    # Default transitions.
    config.enter_transition = None
    config.exit_transition = dissolve
    config.intra_transition = None
    config.main_game_transition = dissolve
    config.game_main_transition = dissolve
    config.end_splash_transition = None
    config.end_game_transition = dissolve
    config.after_load_transition = dissolve
    config.window_show_transition = None
    config.window_hide_transition = None
    config.exit_replay_transition = dissolve

    # Customizations/hacks.
    config.image_cache_size = 16
    store._game_menu_screen = "pause_menu"
    config.quit_action = Quit()
    renpy.add_layer(layer="phone", below="screens")
