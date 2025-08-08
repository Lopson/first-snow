# ui.rpy
# Contains the basic user interface screens and elements.

###
#
# Auxiliary Python code.
#
###

init python:
    def set_screen_var(n, v):
        renpy.current_screen().scope[n] = v
        renpy.restart_interaction()

    def get_screen_var(n):
        return renpy.current_screen().scope[n]

    def lang_img(fn):
        # TODO This needs to be removed.
        """
        Tries to see if there's a file whose name ends with "-" + get_language().
        If there is, then that means that the image that should be loaded is the
        one belonging to the language obtained; if not, simply return the given
        argument.
        """
        base, ext = fn.rsplit('.', 1)
        lfn = base + '-' + GameContext.get_language() + '.' + ext
        if renpy.loadable(lfn):
            return lfn
        else:
            return fn

###
#
# Screens.
#
###

########################################################################################
# Main screens.
########################################################################################

# Our main menu screen.
screen main_menu():
    tag menu
    on "show" action Play('music', get_menu_theme(), if_changed=True)

    window:
        style "mm_root"
        background "#000000"
        if persistent.finished_story:
            add "ui/main/bg-together-at-last.webp" at tdissolve(1.25)
        else:
            add "ui/main/bg.webp" at tdissolve(1.25)
        add "snow light" at tdissolve(1.5)

        if renpy.get_screen('load') or renpy.get_screen('preferences') or renpy.get_screen('extras'):
            add "ui/overlay.webp" at tdissolve(0.7)

    frame:
        background Null()
        left_padding 0
        top_padding 0

    use sub_menu

# The pause menu screen.
screen pause_menu():
    tag menu

    python:
        # Fetch current song.
        trackfile = renpy.music.get_playing('music')
        track = tracks.get(trackfile)
        if track:
            track = track.title

        # Fetch current scene.
        title = game_context.get_scene_title(store.current_scene)

        if GameContext.in_replay():
            title = '{color=#faf6e780}' + _('Replay:') + '{/color} ' + title

        # Fetch current running time.
        runtime = renpy.get_game_runtime()
        time = "%d:%02d" % (int(runtime / 3600), int(runtime / 60) % 60)

    frame:
        background "ui/overlay.webp" at tdissolve(0.5)
        left_padding 0
        top_padding 0

        if not any(renpy.get_screen(x) for x in ('preferences', 'save', 'load', 'extras')):
            # Our song, scene and playtime.
            add "ui/pause/splash.webp":
                xpos 375
                ypos 292

            text (title or _('Unknown scene')) id "title":
                xpos 851
                ypos 330
                size 31
                outlines [(6, '#292d34', 0, 0)]
                color ("#faf6e7" if title else "#faf6e780")

            text (track or _('Nothing playing')) id "track":
                xpos 857
                ypos 368
                size 31
                outlines [(6, '#292d34', 0, 0)]
                color ("#faf6e7" if track else "#faf6e780")

            text time id "time":
                xpos 847
                ypos 292
                size 31
                outlines [(6, '#292d34', 0, 0)]
                color ("#faf6e7" if not GameContext.in_replay() else "#faf6e780")

            textbutton _("View History"):
                xpos 920
                ypos 450
                background "ui/pause/history.webp"
                left_padding 53
                top_padding 8
                text_size 29
                text_color "#faf6e7"
                text_hover_outlines [(3, "#4b565f", 0, 0)]
                text_hover_xoffset -3
                text_hover_yoffset -3
                action ToggleScreen('text_log')

            python:
                if len(config.keymap['text_log']) > 1:
                    km_title = _('keybinds: ')
                    km_binds =  ', '.join(ukm_binding_to_friendly(b) for b in config.keymap['text_log'])
                elif len(config.keymap['text_log']) == 1:
                    km_title = _('keybind: ')
                    km_binds = ukm_binding_to_friendly(config.keymap['text_log'][0])
                else:
                    km_title = ''
                    km_binds = ''
            text km_title + km_binds:
                xpos 958
                ypos 440
                outlines [(3, '#292d34', 0, 0)]
                color "#faf6e7"
                size 17


    use sub_menu

screen sub_menu():
    tag submenu

    use side_menu

screen side_menu():
    tag side_menu

    $ has_subscreen = any(renpy.get_screen(x) for x in ('save', 'load', 'preferences', 'extras'))
    add "ui/side/side.webp":
        xpos 0
        ypos 0

    if not has_subscreen:
        if store.dlc_packages:
            add lang_img("ui/side/logo-dlc.webp"):
                xpos 0
                ypos 0
        else:
            add lang_img("ui/side/logo.webp"):
                xpos 0
                ypos 0

    imagebutton:
        idle "menu_quit_reverse"
        hover "menu_quit_normal"
        xpos 0
        ypos 604
        focus_mask "ui/side/menu_quit_mask.webp"
        hovered ResetDisplayable('menu_quit_normal')
        unhovered ResetDisplayable('menu_quit_reverse')
        action Quit(confirm=True)

    if not game_context.in_playthrough():
        add lang_img("ui/side/menu_new.webp"):
            xpos 110
            ypos 193

        imagebutton:
            idle "menu_newgame_init"
            hover "menu_newgame"
            xpos 110
            ypos 193
            hovered ResetDisplayable('menu_newgame')
            action [
                Stop('jukebox', fadeout=1.0),
                Play('music', get_menu_theme(), fadein=1.0, if_changed=True),
                Hide('menu'),
                Hide('side_menu', transition=dissolve),
                Start()
            ]
            activate_sound "sfx/turning-pages.ogg"
    else:
        if GameContext.in_replay():
            add Transform(lang_img("ui/side/menu_save.webp"), alpha=0.5):
                xpos 110
                ypos 193

            imagebutton:
                idle Transform("menu_savegame_init", alpha=0.5)
                xpos 110
                ypos 193
        else:
            imagebutton:
                idle lang_img("ui/side/menu_save.webp")
                selected_idle lang_img("ui/side/menu_back1.webp")
                xpos 110
                ypos 193
                action ToggleScreen('save', fastDissolve)

            imagebutton:
                idle "menu_savegame_init"
                hover "menu_savegame"
                selected_idle "menu_savegame_back_init"
                selected_hover "menu_savegame_back"
                xpos 110
                ypos 193
                hovered [
                    ResetDisplayable('menu_savegame'),
                    ResetDisplayable('menu_savegame_back')
                ]
                action ToggleScreen('save', fastDissolve)

    imagebutton:
        idle lang_img("ui/side/menu_load.webp")
        selected_idle lang_img("ui/side/menu_back2.webp")
        xpos 8
        ypos 310
        action ToggleScreen('load', fastDissolve)

    imagebutton:
        idle "menu_loadgame_init"
        hover "menu_loadgame"
        selected_idle "menu_loadgame_back_init"
        selected_hover "menu_loadgame_back"
        xpos 8
        ypos 310
        hovered [
            ResetDisplayable('menu_loadgame'),
            ResetDisplayable('menu_loadgame_back')
        ]
        action ToggleScreen('load', fastDissolve)

    imagebutton:
        idle lang_img("ui/side/menu_options.webp")
        selected_idle lang_img("ui/side/menu_back3.webp")
        xpos 109
        ypos 420
        action ToggleScreen('preferences', fastDissolve)

    imagebutton:
        idle "menu_options_init"
        hover "menu_options"
        selected_idle "menu_options_back_init"
        selected_hover "menu_options_back"
        xpos 109
        ypos 420
        hovered [
            ResetDisplayable('menu_options'),
            ResetDisplayable('menu_options_back')
        ]
        action ToggleScreen('preferences', fastDissolve)

    if game_context.in_playthrough():
        add lang_img("ui/side/menu_main.webp"):
            xpos -7
            ypos 530

        imagebutton:
            idle "menu_mainmenu_init"
            hover "menu_mainmenu"
            xpos -7
            ypos 530
            hovered ResetDisplayable('menu_mainmenu')

            if not GameContext.in_replay():
                action MainMenu()
            else:
                action [EndReplay()]
    else:
        imagebutton:
            idle lang_img("ui/side/menu_extras.webp")
            selected_idle lang_img("ui/side/menu_back4.webp")
            xpos -7
            ypos 530
            action ToggleScreen('extras', fastDissolve)

        imagebutton:
            idle "menu_extras_init"
            hover "menu_extras"
            selected_idle "menu_extras_back_init"
            selected_hover "menu_extras_back"
            xpos -7
            ypos 530
            hovered [
                ResetDisplayable('menu_extras'),
                ResetDisplayable('menu_extras_back')
            ]
            action ToggleScreen('extras', fastDissolve)

    add "ui/side/pins.webp"



########################################################################################
# Preferences.
########################################################################################

screen preferences():
    tag submenu
    on "show" action Show('preferences_general')
    on "replace" action Show('preferences_general')
    on "hide" action Hide('prefmenu')
    on "replaced" action Hide('prefmenu')
    key "mousedown_3" action Hide('preferences', dissolve)

    frame:
        background Null()
        
        add "ui/tab.webp":
            xalign 1.0
            xoffset 10
            ypos 50

        textbutton __("General"):
            text_size 30
            xpos 680
            ypos 52
            selected_left_padding 9
            background Null()
            selected_background "ui/preferences/sections/general.webp"
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('preferences_general', fastDissolve)

        textbutton __("Keybinds"):
            text_size 30
            xpos 810
            ypos 52
            selected_left_padding 9
            background Null()
            selected_background "ui/preferences/sections/keybinds.webp"
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('preferences_keymap', fastDissolve)

        textbutton __("Voices"):
            text_size 30
            xpos 950
            ypos 52
            selected_left_padding 9
            background Null()
            selected_background "ui/preferences/sections/voices.webp"
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('preferences_voices', fastDissolve)

        textbutton __("Accessibility"):
            text_size 30
            xpos 1060
            ypos 52
            selected_left_padding 9
            background Null()
            selected_background "ui/preferences/sections/accessibility.webp"
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('preferences_accessibility', fastDissolve)

    use side_menu

    add "ui/preferences/options.webp" at trotate(-10):
        xpos 165
        ypos 82

    text __("Options") at trotate(-10):
        size 72
        color "#faf6e7"
        xpos 240
        ypos -20


# General preferences.

screen preferences_general():
    tag prefmenu
    
    frame:
        background Null()
        xpos 300

        if store.h_available:
            add "ui/preferences/icons/adult_content.webp":
                xpos 45
                ypos 190

            text __("Adult content"):
                color "#faf6e7"
                size 24
                xpos 85
                ypos 190

            imagebutton:
                idle "ui/preferences/checkbox.webp"
                hover "ui/preferences/checkbox-hover.webp"
                selected_idle "ui/preferences/checkbox-checked.webp"
                selected_hover "ui/preferences/checkbox-checked-hover.webp"
                xpos 725
                hover_xpos 724
                selected_xpos 724
                ypos 188
                selected persistent.h
                action [
                    SetVariable('persistent.h', not persistent.h),
                    SetVariable('store.allow_explicit', not persistent.h),
                    renpy.partial(achievement.grant, 'h')
                ]

        add "ui/preferences/icons/fullscreen.webp":
            xpos 45
            ypos 225

        text __("Fullscreen"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 225

        imagebutton:
            selected game.preferences.fullscreen
            idle "ui/preferences/checkbox.webp"
            hover "ui/preferences/checkbox-hover.webp"
            selected_idle "ui/preferences/checkbox-checked.webp"
            selected_hover "ui/preferences/checkbox-checked-hover.webp"
            xpos 725
            hover_xpos 724
            selected_xpos 724
            ypos 223
            action renpy.toggle_fullscreen

        add "ui/preferences/icons/theme.webp":
            xpos 45
            ypos 260

        text __("Theme"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 260

        textbutton __("Story"):
            xpos 527
            ypos 258
            text_size 24
            left_padding 3
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/story.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'ui_season', None)

        textbutton __("Fall"):
            xpos 617
            ypos 258
            text_size 24
            left_padding 3
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/story_fall.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'ui_season', 'fall')

        textbutton __("Winter"):
            xpos 675
            ypos 254
            text_size 24
            left_padding 3
            top_padding 4
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/story_winter.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'ui_season', 'winter')

        add "ui/preferences/divider.webp":
            xpos 40
            ypos 305

        add "ui/preferences/icons/text_speed.webp":
            xpos 45
            ypos 320

        text __("Text speed"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 320

        add "ui/preferences/bar.webp":
            xpos 480
            ypos 320

        bar value Preference('text speed'):
            xpos 481
            ypos 320
            xmaximum 270
            left_bar Null()
            right_bar Null()
            thumb 'ui/preferences/bar_handle.webp'

        add "ui/preferences/icons/skip_all.webp":
            xpos 45
            ypos 355

        text __("Skip unseen dialogue"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 355

        imagebutton:
            idle "ui/preferences/checkbox.webp"
            hover "ui/preferences/checkbox-hover.webp"
            selected_idle "ui/preferences/checkbox-checked.webp"
            selected_hover "ui/preferences/checkbox-checked-hover.webp"
            xpos 725
            ypos 353
            hover_xpos 724
            selected_xpos 724
            action ToggleField(game.preferences, 'skip_unseen')

        add "ui/preferences/icons/auto_continue.webp":
            xpos 45
            ypos 390

        text __("Auto-continue"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 390

        imagebutton:
            idle "ui/preferences/checkbox.webp"
            hover "ui/preferences/checkbox-hover.webp"
            selected_idle "ui/preferences/checkbox-checked.webp"
            selected_hover "ui/preferences/checkbox-checked-hover.webp"
            xpos 725
            ypos 388
            hover_xpos 724
            selected_xpos 724
            action ToggleField(game.preferences, 'afm_enable')

        add "ui/preferences/icons/auto_continue_time.webp":
            xpos 45
            ypos 425

        text __("Auto-continue wait time"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 425

        add "ui/preferences/bar.webp":
            xpos 480
            ypos 425

        bar value Preference('auto-forward time'):
            xpos 481
            ypos 425
            xmaximum 270
            left_bar Null()
            right_bar Null()
            thumb 'ui/preferences/bar_handle.webp'

        add "ui/preferences/divider.webp":
            xpos 40
            ypos 465

        add "ui/preferences/icons/volume_music.webp":
            xpos 45
            ypos 480

        text __("Music"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 480

        add "ui/preferences/bar.webp":
            xpos 480
            ypos 480

        bar value Preference('music volume'):
            xpos 481
            ypos 480
            xmaximum 270
            left_bar Null()
            right_bar Null()
            thumb 'ui/preferences/bar_handle.webp'

        add "ui/preferences/icons/volume_ambience.webp":
            xpos 45
            ypos 515

        text __("Ambience"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 515

        add "ui/preferences/bar.webp":
            xpos 480
            ypos 515

        bar value Preference('ambiance volume'):
            xpos 481
            ypos 515
            xmaximum 270
            left_bar Null()
            right_bar Null()
            thumb 'ui/preferences/bar_handle.webp'

        add "ui/preferences/icons/volume_sfx.webp":
            xpos 45
            ypos 550

        text __("Sound effects"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 550

        add "ui/preferences/bar.webp":
            xpos 480
            ypos 550

        bar value Preference('sound volume'):
            xpos 481
            ypos 550
            xmaximum 270
            left_bar Null()
            right_bar Null()
            thumb 'ui/preferences/bar_handle.webp'

        if config.developer or config.testing:
            label '{} v{}-{} - {}'.format(config.name, config.version, git_version(), renpy.version()):
                xpos 400
                ypos 680
                text_color "#faf6e780"


# Keybinds.

screen preferences_keymap():
    tag prefmenu
    on "hide" action Hide('preferences_keymap_add')
    on "replaced" action Hide('preferences_keymap_add')

    add "ui/preferences/icons/reset.webp":
        xpos 1040
        ypos 125
    
    textbutton __("Reset all"):
        background Null()
        text_color "#faf6e7"
        text_size 32
        xpos 1055
        ypos 122
        text_hover_outlines [(3, "#292d34", 0, 0)]
        action ResetUserKeyBindings()

    side "c r":
        xpos 330
        ypos 180
        xsize 900
        ysize 550

        viewport id "preferences_keymap_keys":
            mousewheel True

            vbox:
                xsize 890
                
                for i, event in enumerate(ukm_event_order):
                    if event is None:
                        null height 40
                    else:
                        hbox:
                            xsize 860

                            label ukm_event_descriptions[event]:
                                text_color "#faf6e7"
                                left_padding 10
                                right_padding 20
                                text_size 24
                            
                            hbox:
                                xalign 1.0

                                frame:
                                    background None
                                    top_margin 0
                                    top_padding 0
                                    bottom_margin 5
                                    hbox:
                                        box_wrap True
                                        box_reverse True
                                        spacing 3

                                        $ bindings = ukm_get_bindings(event)

                                        for sym, name, joy in reversed(bindings):
                                            if name:
                                                textbutton renpy_quote(name.lower()):
                                                    background "#faf6e7"
                                                    text_color "#4e585f"
                                                    hover_background "#faf6e780"
                                                    action renpy.partial(ukm_remove_binding, event, sym, joy)
                                                    xpadding 10
                                                    top_margin 5
                                                    text_size 16
                                                    xalign 1.0

                                if len(bindings) >= 5:
                                    imagebutton:
                                        idle "ui/preferences/icons/capped.webp"
                                        top_margin 8
                                        left_margin 5
                                        right_margin 12
                                        bottom_margin 18
                                else:
                                    textbutton "+":
                                        background Null()
                                        text_color "#faf6e780"
                                        text_hover_color "#faf6e7"
                                        text_size 32
                                        top_margin -5
                                        left_margin -5
                                        action Show('preferences_keymap_add', dissolve, event)

                        if i < len(ukm_event_order) - 1 and ukm_event_order[i + 1]:
                            add "ui/preferences/keybinds/divider.webp"
                            null height 10

                null height 50

        vbar value YScrollValue('preferences_keymap_keys'):
            top_bar "ui/preferences/scrollbar.webp"
            bottom_bar "ui/preferences/scrollbar.webp"
            thumb "ui/preferences/scrollbar_handle.webp"
            ymaximum 493
            xmaximum 30
            top_gutter 10
            bottom_gutter 10


screen preferences_keymap_add(event):
    python:
        if not hasattr(store, '_keymap_captured_key') or not store._keymap_captured_key:
            store._keymap_captured_key = (None, None, None)

        binding, name, joy = store._keymap_captured_key
        if not name:
            name = '(nothing)'

    frame:
        background "ui/pause/overlay.webp"

    frame id "preferences_keymap_add_frame":
        background "ui/yesno/bg.webp"
        xpadding 284
        ypadding 192

        add KeyBindingGrabBehaviour('_keymap_captured_key', exclude_displayables=['keymap_add_ok', 'keymap_add_cancel'])

        text __("Please press the keys or buttons you want to bind."):
            yoffset 50
            size 30
            xmaximum 680
            text_align 0.5
            xalign 0.5
            color "#24282d"

        text renpy_quote(name):
            yoffset 100
            size 42
            xmaximum 680
            text_align 0.5
            xalign 0.5
            color "#24282d"

        imagebutton id "keymap_add_ok":
            idle lang_img("ui/yesno/yes.webp")
            hover lang_img("ui/yesno/yes_hover.webp")
            focus_mask True
            xoffset 455
            yoffset 181
            action [
                AddUserKeyBinding(event, binding, joy),
                Hide('preferences_keymap_add', fastDissolve),
                Delayed(0.5, SetVariable('_keymap_captured_key', None))
            ]

        imagebutton id "keymap_add_cancel":
            idle lang_img("ui/yesno/no.webp")
            hover lang_img("ui/yesno/no_hover.webp")
            focus_mask True
            xoffset 588
            yoffset 180
            action [
                Hide('preferences_keymap_add', fastDissolve),
                Delayed(0.5, SetVariable('_keymap_captured_key', None))
            ]

init python:
    def update_h_val(new_y):
        set_screen_var('h_val', new_y)

screen preferences_voices():
    tag prefmenu

    default h_val = 0

    python:
        adj = ui.adjustment(changed=update_h_val)

    vbox:
        xpos 339
        ypos 229

        frame:
            background "ui/preferences/voices/bg.webp"
            xsize 767
            ysize 420
            padding (0, 0)

            viewport id "preferences_voices_characters":
                xpos 57
                xsize 717
                xadjustment adj
                mousewheel "horizontal"

                hbox:
                    for (tag, name, vo, color) in store.voices:
                        python:
                            sample = 'voice/test_' + tag + '.mp3'
                            event = ExtendableEvent(1.0,
                                start_func=renpy.partial(play_vo_test, tag, sample),
                                stop_func=renpy.partial(stop_vo_test, tag)
                            )
                            voice_adj = ui.adjustment(range=1.0, value=GetCharacterVolume(tag),
                                changed=renpy.partial(sustain_vo_test, event, tag, 1.0)
                            )
                            topbar = Composite((160, 346),
                                (0, 0), "ui/preferences/voices/bar_{}.webp".format(tag),
                                (0, 0), Transform("ui/preferences/voices/bar.webp", alpha=0.6)
                            )
                        fixed:
                            xsize 197

                            vbar value SetCharacterVolume(tag):
                                adjustment voice_adj
                                xpos 0
                                ypos 28
                                xysize (160, 346)
                                top_bar topbar
                                bottom_bar "ui/preferences/voices/bar_{}.webp".format(tag)

                            vbar value SetCharacterVolume(tag):
                                adjustment voice_adj
                                xpos 165
                                ypos 16
                                xysize (23, 373)
                                base_bar Null()
                                thumb "ui/preferences/voices/indicator.webp"

                            text "[name]":
                                size 24
                                color color
                                outlines [(2, "#faf6e7", 0, 0)]
                                xpos 168
                                ypos 351
                                xanchor 1.0

                            text "[vo]":
                                size 16
                                color color
                                outlines [(2, "#faf6e7", 0, 0)]
                                xpos 164
                                ypos 383
                                xanchor 1.0

        bar value XScrollValue("preferences_voices_characters"):
            xpos 50
            xsize 711
            ysize 40
            left_bar 'ui/preferences/voices/slider-bg.webp'
            right_bar 'ui/preferences/voices/slider-bg.webp'
            thumb 'ui/preferences/voices/slider-handle.webp'

    text __("Volume Settings"):
        size 48
        color "#faf6e7"
        outlines [(5, "#292d34", 0, 0)]
        xpos 355
        ypos 185

    imagebutton:
        idle "ui/preferences/checkbox.webp"
        hover "ui/preferences/checkbox-hover.webp"
        selected_idle "ui/preferences/checkbox-checked.webp"
        selected_hover "ui/preferences/checkbox-checked-hover.webp"
        xpos 964
        ypos 205
        hover_xpos 963
        selected_xpos 963
        action Preference('emphasize audio', 'toggle')

    text __("Emphasize voices"):
        color "#faf6e7"
        outlines [(1, "#292d34", 0, 0)]
        ypos 210
        xpos 994
        size 20

screen preferences_accessibility():
    tag prefmenu
    
    frame:
        background Null()
        xpos 300

        text __("* Changes only apply to textbox and pop-ups"):
            color "#faf6e7"
            size 16
            xpos 750
            xanchor 1.0
            ypos 195

        add "ui/preferences/icons/text_color.webp":
            xpos 45
            ypos 225

        text __("Text color"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 225

        textbutton __("Standard"):
            xpos 547
            ypos 223
            text_size 24
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/standard.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'high_contrast', False)

        textbutton __("Black"):
            xpos 690
            ypos 223
            text_size 24
            left_padding 5
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/black.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'high_contrast', True)

        add "ui/preferences/icons/text_font.webp":
            xpos 45
            ypos 260

        text __("Text font"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 260

        textbutton __("Standard"):
            xpos 330
            ypos 258
            text_size 24
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/standard.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'font_mode', 'standard')

        textbutton __("Sans-serif"):
            xpos 460
            ypos 257
            text_size 28
            background Null()
            top_padding -4
            left_padding 5
            text_color "#fcf9ea"
            text_font "ui/BalooTamma2-Medium.ttf"
            selected_background "ui/preferences/sections/sansserif.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'font_mode', 'sans')

        textbutton __("OpenDyslexic"):
            xpos 595
            ypos 258
            text_size 20
            left_padding 15
            background Null()
            text_color "#fcf9ea"
            text_font "ui/OpenDyslexic3.ttf"
            selected_background "ui/preferences/sections/opendyslexic.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            top_padding -8
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'font_mode', 'dyslexia')

        add "ui/preferences/divider.webp":
            xpos 40
            ypos 303

        add "ui/preferences/icons/cue_music.webp":
            xpos 45
            ypos 320

        text __("Music Cues"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 320

        imagebutton:
            idle "ui/preferences/checkbox.webp"
            hover "ui/preferences/checkbox-hover.webp"
            selected_idle "ui/preferences/checkbox-checked.webp"
            selected_hover "ui/preferences/checkbox-checked-hover.webp"
            xpos 725
            ypos 318
            hover_xpos 724
            selected_xpos 724
            action ToggleField(persistent, 'cue_music')

        add "ui/preferences/icons/cue_sfx.webp":
            xpos 45
            ypos 355

        text __("Sound Cues"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 355

        imagebutton:
            idle "ui/preferences/checkbox.webp"
            hover "ui/preferences/checkbox-hover.webp"
            selected_idle "ui/preferences/checkbox-checked.webp"
            selected_hover "ui/preferences/checkbox-checked-hover.webp"
            xpos 725
            ypos 351
            hover_xpos 724
            selected_xpos 724
            action ToggleField(persistent, 'cue_sfx')

        add "ui/preferences/icons/tts.webp":
            xpos 45
            ypos 390

        text __("Text-to-speech"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 390

        imagebutton:
            idle "ui/preferences/checkbox.webp"
            hover "ui/preferences/checkbox-hover.webp"
            selected_idle "ui/preferences/checkbox-checked.webp"
            selected_hover "ui/preferences/checkbox-checked-hover.webp"
            xpos 725
            ypos 386
            hover_xpos 724
            selected_xpos 724
            action ToggleField(game.preferences, 'self_voicing')

        add "ui/preferences/divider.webp":
            xpos 40
            ypos 431

        add "ui/preferences/icons/theme.webp":
            xpos 45
            ypos 444

        text __("Cues Theme"):
            color "#faf6e7"
            size 24
            xpos 85
            ypos 444

        textbutton __("Story"):
            xpos 527
            ypos 442
            text_size 24
            left_padding 3
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/story.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'cue_season', None)

        textbutton __("Fall"):
            xpos 617
            ypos 442
            text_size 24
            left_padding 3
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/story_fall.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'cue_season', 'fall')

        textbutton __("Winter"):
            xpos 675
            ypos 438
            text_size 24
            left_padding 3
            top_padding 4
            background Null()
            text_color "#fcf9ea"
            selected_background "ui/preferences/sections/story_winter.webp"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#292d34", 0, 0)]
            text_selected_hover_outlines []
            hover_xoffset -3
            hover_yoffset -3
            selected_hover_xoffset 0
            selected_hover_yoffset 0
            action SetField(persistent, 'cue_season', 'winter')



########################################################################################
# Extras.
########################################################################################

screen extras():
    tag submenu
    on "show" action Show('extras_scenes')
    on "replace" action Show('extras_scenes')
    on "hide" action Hide('extramenu')
    on "replaced" action Hide('extramenu')
    key "mousedown_3" action Hide('extras', dissolve)

    frame:
        background Null()

        add "ui/tab.webp":
            xalign 1.0
            xoffset 10
            ypos 49

        textbutton _("Scene Select"):
            text_size 30
            xpos 730
            ypos 53
            selected_left_padding 15
            background Null()
            selected_background "ui/extras/tab-scenes.webp"
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('extras_scenes', fastDissolve)

        textbutton _("Gallery"):
            text_size 30
            xpos 950
            ypos 53
            selected_left_padding 15
            background Null()
            selected_background Transform("ui/extras/tab-gallery.webp", xoffset=-5)
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('extras_art', fastDissolve)

        textbutton _("Jukebox"):
            text_size 30
            xpos 1090
            ypos 53
            selected_left_padding 9
            background Null()
            selected_background "ui/extras/tab-jukebox.webp"
            text_color "#faf6e7"
            text_selected_color "#4e585f"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_selected_hover_outlines []
            action Show('extras_music', fastDissolve)

    use side_menu

    add "ui/extras/extras.webp" at trotate(-20):
        xpos 185
        ypos 70

    text _("Extras") at trotate(-10):
        size 72
        color "#faf6e7"
        xpos 260
        ypos -12


## Scenes.

init python:
    def calculate_extra_cutoffs(new_y):
        act_cutoffs = [(1345, 4), (900, 3), (410, 2), (0, 1)]
        act_y, act_cutoff = [(y, a) for (y, a) in act_cutoffs if new_y >= y][0]
        scene_cutoff = (new_y - act_y + 30) // 45
        set_screen_var('cutoff_act', act_cutoff)
        set_screen_var('cutoff_scene', scene_cutoff)

screen extras_scenes():
    tag extramenu

    default current_act = 1
    default current_scene = 1
    default cutoff_act = 1
    default cutoff_scene = 1
    default hidden_act_cutoff = 4

    $ current_label = '{}S{}'.format(current_act, current_scene)
    $ yadj = ui.adjustment(changed=calculate_extra_cutoffs)
    python:
        acts_seen = game_context.acts_seen()
        if acts_seen:
            max_act = max(acts_seen)
        else:
            max_act = 0

    hbox:
        xpos 355
        ypos 150
        xsize 730
        ysize 700

        frame:
            background Transform("ui/extras/scenes/list-bg.webp", yoffset=25)
            ysize 500
            xsize 380

            viewport id "extras_scene_gallery":
                xoffset 2
                ysize 500
                mousewheel True
                yadjustment yadj

                vbox:
                    spacing 1
                    for act in range(1, (max_act + 1)):
                        python:
                            from collections import OrderedDict
                            act_scenes = OrderedDict([(scene, game_context.get_scene_title(scene)) for scene in scene_titles if scene.startswith(str(act) + 'S')])
                        text (__("Act") + " {}".format(game_context.get_act_title(act)) if act > cutoff_act else " "):
                            size 65
                            xoffset 3
                            outlines [(4, "#292d34", 0, 0)]
                        for x in enumerate(act_scenes, 1):
                            # NOTE The variable "scene_label" actually contains the xSy identifier and not the scripting label.
                            $ i, scene_label = x
                            $ sceneshot = "scripts/sceneshots/" + scene_label + ".webp"

                            if act < cutoff_act or (act == cutoff_act and i < cutoff_scene):
                                null height 44
                            elif game_context.scene_seen(scene_label):
                                fixed:
                                    ysize 44

                                    imagebutton:
                                        idle Transform(sceneshot, xoffset=2, yoffset=2)
                                        hover Composite((353, 44), (0, 0), "#4b565f", (2, 2), sceneshot)
                                        selected (current_label == scene_label)
                                        selected_idle Composite((353, 44), (0, 0), "#fbf9ec", (2, 2), sceneshot)
                                        selected_hover Composite((353, 44), (0, 0), "#fbf9ec", (2, 2), sceneshot)
                                        xysize (353, 44)
                                        action [
                                            SetLocalVariable('current_act', act),
                                            SetLocalVariable('current_scene', i)]

                                    text "{}. {}".format(i, game_context.get_scene_title(scene_label)):
                                        size 21
                                        color "#fbf9ec"
                                        outlines [(2, "#4b565f", 0, 0)]
                                        xpos 2
                                        ypos 49
                                        yanchor 1.0
                            else:
                                fixed:
                                    ysize 44

                                    imagebutton:
                                        idle "ui/extras/scenes/locked.webp"
                                        action None
                                        xpos 2
                                        ypos 2
                    
                    null height 40

            text __("Act ") + str(cutoff_act):
                size 65
                outlines [(4, "#292d34", 0, 0)]
                xoffset 5

            add "ui/extras/scenes/list-tail.webp":
                ypos 1.0
                yanchor 0.0
                xoffset -5
                yoffset 3

        vbar value YScrollValue('extras_scene_gallery'):
            top_bar "ui/extras/scrollbar.webp"
            bottom_bar "ui/extras/scrollbar.webp"
            thumb "ui/preferences/scrollbar_handle.webp"
            yminimum 475
            ymaximum 475
            xmaximum 30
            top_gutter 25
            bottom_gutter 25
            unscrollable "hide"
            yoffset 25
            xoffset -5

        if game_context.scene_seen(current_label):
            frame:
                background ("scripts/sceneshots/" + current_label + "_full.webp")
                xsize 482
                ysize 521

                imagebutton:
                    idle Transform("ui/extras/scenes/read.webp", xoffset=4, yoffset=7)
                    hover Composite((102, 65), (0, 0), "ui/extras/scenes/read-hover.webp", (4, 7), "ui/extras/scenes/read.webp")
                    action [
                        Stop('music', fadeout=1.0),
                        Replay("scene_" + current_label)
                    ]
                    xpos 328
                    ypos 473
                
                text scene_descriptions[current_label]:
                    ypos 430
                    xpos 20
                    size 21
                    xmaximum 300
                    color "#fbf9ec"
                    outlines [(2, "#292d35", 0, 0)]

## Art gallery.

screen extras_art():
    tag extramenu
    on "show" action Show('extras_art_firstsnow')
    on "replace" action Show('extras_art_firstsnow')
    on "hide" action Hide('extraartmenu')
    on "replaced" action Hide('extraartmenu')

    frame:
        background Null()
        xpos 300
        
        textbutton __("CGs"):
            background Transform("ui/extras/gallery/tab-cg.webp", yoffset=5)
            action Show('extras_art_firstsnow', fastDissolve)
            ypos 93
            xpos 675
            text_size 30
            text_color "#a1aab1"
            text_selected_color "#fbf9ec"
            text_hover_outlines [(1, "#4b565f", 0, 0)]
            text_selected_hover_outlines []

        textbutton __("Guest Art"):
            background Transform("ui/extras/gallery/tab-guest.webp", yoffset=8)
            action Show('extras_art_extra', fastDissolve)
            ypos 93
            xpos 775
            text_size 30
            text_color "#a1aab1"
            text_selected_color "#fbf9ec"
            text_hover_outlines [(1, "#4b565f", 0, 0)]
            text_selected_hover_outlines []

screen extras_art_firstsnow():
    tag extraartmenu

    use extras_art_gallery(pieces=store.cg_art, art_type='cg')

screen extras_art_extra():
    tag extraartmenu

    use extras_art_gallery(pieces=store.guest_art, art_type='guest', show_info=True)

screen extras_art_gallery(pieces, art_type, show_info=False):
    python:
        from copy import deepcopy
        from math import ceil
        from renpy.display.predict import predicting

        # Let's have each piece determine on the spot if it's
        # locked/visible and its thumbnails if necessary.
        pieces = deepcopy(pieces)
        for piece in pieces:
            piece.eval_piece()
        
        # This filters out the "H" DLC pieces and locked pieces.
        pieces: list = [p for p in pieces if p.is_visible and not p.locked]
        rows: int = int(ceil(len(pieces) / 2.0))

        if not predicting and art_type == 'guest':
            achievement.grant('art_guest_viewed')

    default current_piece = pieces[0] if not pieces[0].locked else None

    hbox:
        xpos 351
        ypos 179
        xsize 900
        ysize 520

        frame:
            background "ui/extras/gallery/list-bg.webp"
            xsize 506
            ysize 517

            viewport id "extras_art_gallery":
                mousewheel True

                xpos 30
                ypos 10
                ysize 488

                vbox:
                    spacing 0

                    grid 2 rows:
                        xspacing 16
                        yspacing 8

                        for piece in pieces:
                            fixed:
                                xsize 208
                                ysize 122

                                if piece.locked:
                                    pass
                                else:
                                    $ thumb = piece.preview if piece.preview else piece.thumb[0]
                                    imagebutton:
                                        idle           Composite((208, 122), (4, 4), thumb)
                                        hover          Composite((208, 122), (0, 0), "#4b565f", (4, 4), thumb)
                                        selected_idle  Composite((208, 122), (0, 0), "#fbf9ec", (4, 4), thumb)
                                        selected_hover Composite((208, 122), (0, 0), "#fbf9ec", (4, 4), thumb)
                                        selected (current_piece == piece)
                                        action SetLocalVariable('current_piece', piece)

                                    if len(piece.file) > 1:
                                        textbutton str(len(piece.file)):
                                            background Transform("ui/extras/gallery/list-variants.webp", xalign=1.0, xoffset=-5)
                                            xalign 1.0
                                            yalign 0.0
                                            xoffset 5
                                            yoffset 3
                                            text_size 20
                                            text_text_align 0.5

                        if len(pieces) % 2 == 1:
                            null height 0 width 0

                    null height 30

            if len(pieces) > 6:
                vbar value YScrollValue('extras_art_gallery'):
                    top_bar "ui/extras/scrollbar.webp"
                    bottom_bar "ui/extras/scrollbar.webp"
                    thumb "ui/preferences/scrollbar_handle.webp"
                    yminimum 465
                    ymaximum 465
                    xmaximum 30
                    top_gutter 10
                    bottom_gutter 10
                    unscrollable "hide"
                    xalign 1.0
                    xoffset 10
                    ypos 30

            add "ui/extras/gallery/list-fade.webp":
                yalign 1.0

        add "ui/extras/gallery/divider.webp":
            yoffset 25
            xalign 0.5

        if current_piece:
            frame:
                xsize 325
                xalign 0.5
                background Transform("ui/extras/gallery/info-bg.webp", yoffset=40, xalign=0.5)

                if not show_info:
                    textbutton __("Variants"):
                        background Transform("ui/extras/gallery/info-header.webp", xoffset=5, yoffset=15)
                        xalign 0.5
                        text_size 48
                        text_color "#faf6e7"
                        text_outlines [(2, "#292d34", 0, 0)]
                    
                    viewport id "extras_art_preview":
                        mousewheel True
                        ysize 488
                        xminimum 325
                        yoffset 53

                        vbox:
                            xminimum 325
                            xalign 0.5
                            spacing 10

                            null height 27

                            for i, f in enumerate(current_piece.thumb):
                                $ zf = Transform(f, zoom=0.75, subpixel=True)
                                frame:
                                    background None
                                    ysize 92
                                    frame:
                                        xalign 0.5
                                        xoffset -20
                                        background "#292d34"
                                        xsize 158
                                        ysize 92
                                        imagebutton:
                                            idle           Composite((154, 90), (2, 2), zf)
                                            hover          Composite((154, 90), (0, 0), "#fbf9ec", (2, 2), zf)
                                            selected_idle  Composite((154, 90), (0, 0), "#fbf9ec", (2, 2), zf)
                                            selected_hover Composite((154, 90), (0, 0), "#fbf9ec", (2, 2), zf)
                                            align (0.5, 0.5)
                                            action Show('extras_art_single', dissolve, current_piece, i)
                                    add "ui/extras/gallery/zoom.webp":
                                        xalign 0.5
                                        xoffset 69
                                        yoffset 65

                            null height 40

                    if len(current_piece.thumb) > 4:
                        vbar value YScrollValue('extras_art_preview'):
                            top_bar "ui/extras/scrollbar.webp"
                            bottom_bar "ui/extras/scrollbar.webp"
                            thumb "ui/preferences/scrollbar_handle.webp"
                            yminimum 435
                            ymaximum 435
                            xmaximum 30
                            top_gutter 10
                            bottom_gutter 10
                            unscrollable "hide"
                            xalign 1.0
                            xoffset 10
                            ypos 60
                else:
                    textbutton __("Info"):
                        background Transform("ui/extras/gallery/info-header.webp", xoffset=-40, yoffset=15)
                        text_size 48
                        text_color "#faf6e7"
                        text_outlines [(2, "#292d34", 0, 0)]
                        xalign 0.5

                    frame:
                        yoffset 80
                        xalign 0.5
                        background "#292d34"
                        xsize 208
                        ysize 120
                        imagebutton:
                            # NOTE Suspicious access of thumb, keep an eye on it.
                            idle  Composite((204, 118), (2, 2), current_piece.thumb)
                            hover Composite((204, 118), (0, 0), "#fbf9ec", (2, 2), current_piece.thumb)
                            align (0.5, 0.5)
                            action Show('extras_art_single', dissolve, current_piece, 0)
                        add "ui/extras/gallery/zoom.webp":
                            xpos 166
                            ypos 90

                    vbox:
                        yoffset 250
                        xoffset 70
                        spacing 30
                        xsize 208

                        vbox:
                            text __("Artist"):
                                size 24
                                color "#faf6e7"
                                outlines [(2, "#292d34", 0, 0)]
                            text (current_piece.author if current_piece.author else __('Anonymous')):
                                size 48
                                color "#faf6e7"
                                outlines [(2, "#292d34", 0, 0)]

                        if current_piece.url:
                            imagebutton:
                                idle "ui/extras/gallery/info-socialmedia.webp"
                                hover "ui/extras/gallery/info-socialmedia-hover.webp"
                                xoffset -30 # "i don't even care anymore" - preserved as a historical artifact.
                                hover_xoffset -29
                                hover_yoffset 1
                                action OpenURL(current_piece.url)

screen extras_art_single(piece, index=0):
    modal True

    default show_native = False

    on "show" action [Show('extras_art_single_overlay', dissolve, piece), SetVariable('_extras_art_single_index', 0)]
    on "hide" action Hide('extras_art_single_overlay', dissolve)
    on "replaced" action Hide('extras_art_single_overlay', dissolve)
    key "mousedown_3" action Hide('extras_art_single', dissolve)
    key "K_ESCAPE" action Hide('extras_art_single', dissolve)

    frame:
        xysize (config.screen_width, config.screen_height)
        background "#292d34"

    viewport:
        mousewheel True
        draggable True
        arrowkeys True
        xinitial 0.5
        yinitial 0.5

        if show_native and piece.native:
            add piece.native[index]
        else:
            fixed:
                xminimum config.screen_width
                ymaximum config.screen_height
                imagebutton:
                    idle piece.file[index]
                    xalign 0.5
                    yalign 0.5
                    action ToggleScreenVariable('show_native')

    key "K_SPACE" action ToggleScreenVariable('show_native')
    key "K_TAB" action ToggleScreen('extras_art_single_overlay', dissolve, piece)
    key "pad_start_press" action ToggleScreenVariable('show_native')
    key "pad_back_press" action ToggleScreen('extras_art_single_overlay', dissolve, piece)

screen extras_art_single_overlay(piece):
    add "ui/extras/gallery/overlay.webp"

    text __("tab/back to toggle menu"):
        xpos 100
        ypos 633
        color "#faf6e7"
        size 13

    if piece.title:
        text '"{}"'.format(piece.title):
            xpos 95
            ypos 649
            color "#faf6e7"
            size 32

    if piece.native:
        text __("space/start to toggle zoom"):
            xpos 100
            ypos 690
            color "#faf6e7"
            size 13

    imagebutton:
        idle "ui/extras/gallery/back.webp"
        hover "ui/extras/gallery/back-hover.webp"
        xpos 30
        ypos 641
        action Hide('extras_art_single', dissolve)

    textbutton _("back"):
        background None
        margin (0, 0)
        padding (0, 0)
        xpos 30
        ypos 671
        text_color "#faf6e7"
        text_size 26
        action Hide('extras_art_single', dissolve)

## Music gallery.

screen extras_music():
    on "replace" action [Stop("music", fadeout=1.0), Show('extras_music_main')]
    on "replaced" action [Stop("jukebox", fadeout=1.0), Play('music', get_menu_theme(), fadein=1.0), Hide('extramusicmenu')]
    on "hide" action [Stop("jukebox", fadeout=1.0), Play('music', get_menu_theme(), fadein=1.0), Hide('extramusicmenu')]

    tag extramenu

    default current_album = 'main'

    frame:
        background Null()

        imagebutton:
            idle Transform("ui/extras/jukebox/album-switch.webp", alpha=0.5)
            hover "ui/extras/jukebox/album-switch.webp"
            selected "ui/extras/jukebox/album-switch-click.webp"
            action [
                SetScreenVariable('current_album', 'event' if current_album == 'main' else 'main'),
                ShowMenu('extras_music_event' if current_album == 'main' else 'extras_music_main'),
                Function(renpy.music.stop, "jukebox")
            ]

            xpos 710
            ypos 144

        if current_album == 'main':
            imagebutton at transparent(0.5):
                idle im.Blur("ui/extras/jukebox/album-event.webp", 1.0)
                selected_idle "ui/extras/jukebox/album-event.webp"
                hover "ui/extras/jukebox/album-event.webp"
                action [
                    SetScreenVariable('current_album', 'event'),
                    ShowMenu('extras_music_event'),
                    Function(renpy.music.stop, "jukebox")
                ]

                xpos 355
                ypos 175

            frame:
                xpos 403
                ypos 199
                xsize 401
                ysize 401

                background "#292d34"

                imagebutton:
                    #idle Transform("ui/extras/jukebox/album-standard.webp", 1.0)
                    idle "ui/extras/jukebox/album-standard.webp"
                    hover "ui/extras/jukebox/album-standard.webp"
                    action [
                        SetScreenVariable('current_album', 'main'),
                        ShowMenu('extras_music_main'),
                        Function(renpy.music.stop, "jukebox")
                    ]

                    xalign 0.5
                    yalign 0.5
        else:
            imagebutton at transparent(0.5):
                idle im.Blur("ui/extras/jukebox/album-standard.webp", 1.0)
                #idle "ui/extras/jukebox/album-standard.webp"
                hover "ui/extras/jukebox/album-standard.webp"
                action [
                    SetScreenVariable('current_album', 'main'),
                    ShowMenu('extras_music_main'),
                    Function(renpy.music.stop, "jukebox")
                ]

                xpos 355
                ypos 175

            frame:
                xpos 403
                ypos 199
                xsize 401
                ysize 401

                background "#292d34"

                imagebutton:
                    idle "ui/extras/jukebox/album-event.webp"
                    selected_idle "ui/extras/jukebox/album-event.webp"
                    hover "ui/extras/jukebox/album-event.webp"
                    action [
                        SetScreenVariable('current_album', 'event'),
                        ShowMenu('extras_music_event'),
                        Function(renpy.music.stop, "jukebox")
                    ]

                    xalign 0.5
                    yalign 0.5

        text (__("Unlockable Tracks") if current_album == 'main' else __("Standard Tracks")):
            color "#faf6e750"
            size 36
            xpos 705
            xalign 1.0
            ypos 190
            yalign 1.0

        text (__("Standard Tracks") if current_album == 'main' else __("Unlockable Tracks")):
            color "#faf6e7"
            size 36
            outlines [(4, "#292d34", 0, 0)]
            xpos 802
            xalign 1.0
            ypos 215
            yalign 1.0


screen extras_music_main():
    tag extramusicmenu
    
    use extras_music_player(music_room=standard_music_room)


screen extras_music_event():
    tag extramusicmenu

    use extras_music_player(music_room=event_music_room, needs_unlock=True)


screen extras_music_player(music_room, needs_unlock=False):
    frame:
        background "ui/extras/jukebox/list-bg.webp"
        xpos 830
        ypos 183
        
        vbox:
            xpos 0
            ypos 20
            spacing 1
            for entry in enumerate(music_room.playlist, 1):
                $ i, track = entry
                $ title = tracks[track].title

                hbox:
                    spacing -2
                    ysize 32
                    if (is_current_mr_playing(music_room) and
                            get_current_mr_track_index(music_room) == i - 1):
                        frame:
                            xoffset 10
                            yoffset 1
                            xsize 50
                            ysize 30
                            background "#faf6e7"
                            top_padding 4
                            add "ui/extras/jukebox/selected-track.webp":
                                xoffset 1
                                yoffset 1

                        textbutton "[title]":
                            background "#faf6e7"
                            text_color "#4e585f"
                            bottom_padding -5
                            ysize 32
                        
                        add "ui/extras/jukebox/selected-track-tail.webp":
                            xoffset 2
                            yoffset -3
                    elif needs_unlock and not music_room.is_unlocked(track):
                        textbutton "[i].":
                            xsize 50
                            ysize 32
                            text_xalign 0.0
                            background None
                            text_color "#faf6e7"
                            text_outlines [(2, "#292d34", 0, 0)]
                            action None
                            bottom_padding -5

                        text _("[[locked!]"):
                            color "#faf6e780"
                            outlines [(2, "#292d3480", 0, 0)]
                    else:
                        python:
                            button_actions = [music_room.Play(track)]
                        textbutton "[i].":
                            xsize 50
                            ysize 32
                            text_xalign 0.0
                            background None
                            text_color "#faf6e7"
                            text_outlines [(2, "#292d34", 0, 0)]
                            action button_actions
                            bottom_padding -5
        
                        textbutton "[title]":
                            background None
                            ysize 32
                            text_color "#faf6e7"
                            text_outlines [(2, "#292d34", 0, 0)]
                            text_hover_outlines [(3, "#4b565f", 0, 0)]
                            hover_xoffset -1
                            action button_actions
                            bottom_padding -5

    fixed:
        xpos 250
        ypos 620
        ysize 100

        add "ui/extras/jukebox/current-song.webp":
            ypos 5

        text (tracks[get_current_mr_track_file(music_room)].title if
                is_current_mr_playing(music_room) else __("Nothing playing")):
            size 24
            xpos 32
            ypos 5
            color ("#faf6e7" if is_current_mr_playing(music_room) else "#faf6e780")

        fixed:
            bar value AudioPositionValue(channel='jukebox'):
                xpos 0
                ypos 40
                xmaximum 305
                left_bar 'ui/extras/jukebox/pos-slider.webp'
                right_bar 'ui/extras/jukebox/pos-slider.webp'
                thumb 'ui/extras/jukebox/pos-handle.webp'

        fixed:
            xpos 330
    
            imagebutton:
                sensitive len(music_room.unlocked_playlist()) > 1
                idle Transform("ui/extras/jukebox/ctrl-back.webp", alpha=0.8)
                hover "ui/extras/jukebox/ctrl-back.webp"
                insensitive Transform("ui/extras/jukebox/ctrl-back.webp", alpha=0.5)
                xpos 0
                
                if not is_current_mr_playing(music_room):
                    action [music_room.Previous()]
                else:
                    action [
                        SetField(music_room, "fadeout", 0.0),
                        SetField(music_room, "fadein", 0.0),
                        music_room.Previous(),
                        SetField(music_room, "fadeout", fadeout_music_room),
                        SetField(music_room, "fadein", fadein_music_room)
                    ]

            imagebutton:
                if (is_current_mr_playing(music_room) and
                        not renpy.music.get_pause(music_room.channel)):
                    idle Transform("ui/extras/jukebox/ctrl-pause.webp", alpha=0.8)
                    hover "ui/extras/jukebox/ctrl-pause.webp"
                else:
                    idle Transform("ui/extras/jukebox/ctrl-play.webp", alpha=0.8)
                    hover "ui/extras/jukebox/ctrl-play.webp"
                
                xpos 50
                if not is_current_mr_playing(music_room):
                    action [music_room.Play()]
                else:
                    action [music_room.TogglePause()]

            imagebutton:
                sensitive len(music_room.unlocked_playlist()) > 1
                idle Transform("ui/extras/jukebox/ctrl-forward.webp", alpha=0.8)
                hover "ui/extras/jukebox/ctrl-forward.webp"
                insensitive Transform("ui/extras/jukebox/ctrl-forward.webp", alpha=0.5)
                xpos 100
                
                if not is_current_mr_playing(music_room):
                    action [music_room.Next()]
                else:
                    action [
                        SetField(music_room, "fadeout", 0.0),
                        SetField(music_room, "fadein", 0.0),
                        music_room.Next(),
                        SetField(music_room, "fadeout", fadeout_music_room),
                        SetField(music_room, "fadein", fadein_music_room)
                    ]

            imagebutton:
                sensitive is_current_mr_playing(music_room)
                idle Transform("ui/extras/jukebox/ctrl-stop.webp", alpha=0.8)
                hover "ui/extras/jukebox/ctrl-stop.webp"
                insensitive Transform("ui/extras/jukebox/ctrl-stop.webp", alpha=0.5)
                xpos 150
                if not renpy.music.get_pause(music_room.channel):
                    action [
                        music_room.Stop(),
                        Delayed(music_room.fadeout, renpy.restart_interaction)
                    ]
                else:
                    action [
                        SetField(music_room, "fadeout", 0.0),
                        music_room.Stop(),
                        SetField(music_room, "fadeout", fadeout_music_room),
                        Function(renpy.restart_interaction)
                    ]

            bar value MixerValue("jukebox"):
                xpos 0
                ypos 40
                xmaximum 185
                left_bar 'ui/extras/jukebox/vol-slider.webp'
                right_bar 'ui/extras/jukebox/vol-slider.webp'
                thumb 'ui/extras/jukebox/vol-handle.webp'

            if preferences.get_mixer("jukebox") > 0.0:
                add "ui/extras/jukebox/volume1.webp":
                    xpos 193
                    ypos 35
            if preferences.get_mixer("jukebox") > 0.333:
                add "ui/extras/jukebox/volume2.webp":
                    xpos 200
                    ypos 23
            if preferences.get_mixer("jukebox") > 0.666:
                add "ui/extras/jukebox/volume3.webp":
                    xpos 203
                    ypos 13



########################################################################################
# Save/load.
########################################################################################

screen saveload(save):
    $ saves = renpy.list_saved_games('[0-9]')

    hbox:
        xpos 470
        ypos 183
        spacing 22

        viewport id "saveload_slots":
            mousewheel True
            xsize 654
            ysize 472

            if save:
                yinitial 1.0

            vbox:
                for i, (name, extra_info, screenshot, time) in enumerate(saves):
                    $ extra = renpy.slot_json(name)
                    $ outdated = extra.get('patch_version', 1) < config.patch_version
                    $ ttitle = game_context.get_scene_title(extra['scene'])
                    $ ttime = int(extra['playtime']) // 60
                    frame:
                        background "ui/saveload/slot.webp"
                        xysize (654, 125)

                        if outdated:
                            add "ui/saveload/broken.webp":
                                xpos 545
                                ypos 15

                        add screenshot:
                            xpos 28
                            ypos 3
                            subpixel True
                            size (181, 102)

                        text "{}.".format(i + 1):
                            xpos 3
                            ypos 56
                            ysize 40
                            color "#faf6e7"
                            size 31
                            text_align 1.0

                        text ttitle:
                            xpos 256
                            ypos 12
                            size 31
                            color "#4b565f"

                        text "{}:{:02}".format(*divmod(ttime, 60)):
                            xpos 256
                            ypos 52
                            size 31
                            color "#4b565f"

                        imagebutton:
                            idle Null()
                            xpos 0
                            ypos 0
                            xysize (654, 125)
                            action If(outdated and not save,
                                Confirm(
                                    'This older save may cause issues. If so, please start\n' +
                                    'a new game and use "Skip unseen text" (in Options)\n' +
                                    'to quickly return to where you were in the story.',
                                    renpy.partial(renpy.load, name),
                                ),
                                renpy.partial(renpy.save if save else renpy.load, name),
                            )

                        imagebutton:
                            idle "ui/saveload/yeet.webp"
                            hover "ui/saveload/yeet-hover.webp"
                            xpos 612
                            ypos 16
                            action renpy.partial(renpy.unlink_save, name)

                if save:
                    imagebutton:
                        idle "ui/saveload/slot-add.webp"
                        xysize (654, 125)
                        action FileSave(None)
                elif not saves:
                    frame:
                        background "ui/saveload/slot-empty.webp"
                        xysize (654, 125)

                        text __("No saves here..."):
                            xalign 0.5
                            yalign 0.5
                            yoffset -18


        if len(saves) > 4 or (save and len(saves) > 3):
            vbar value YScrollValue('saveload_slots'):
                top_bar "ui/preferences/scrollbar.webp"
                bottom_bar "ui/preferences/scrollbar.webp"
                thumb "ui/preferences/scrollbar_handle.webp"
                ymaximum 472
                xmaximum 30
                top_gutter 10
                bottom_gutter 10

# The file save screen.
screen save():
    tag submenu
    key "mousedown_3" action Hide('save', dissolve)

    frame:
        background Null()

        add "ui/tab.webp":
            xalign 1.0
            xoffset 10
            ypos 50

        use saveload(save=True)

    use side_menu

    add "ui/saveload/save.webp":
        xpos 250
        ypos 81

    text _("Save") at trotate(-10):
        xpos 300
        ypos 3
        size 72
        color "#faf6e7"

# The file load screen.
screen load():
    tag submenu
    key "mousedown_3" action Hide('load', dissolve)

    frame:
        background Null()

        add "ui/tab.webp":
            xalign 1.0
            xoffset 10
            ypos 50

        use saveload(save=False)

    use side_menu

    add "ui/saveload/load.webp":
        xpos 250
        ypos 85

    text _("Load") at trotate(-10):
        xpos 300
        ypos 10
        size 72
        color "#faf6e7"


########################################################################################
# Misc.
########################################################################################

# General yes/no prompt.
screen yesno_prompt(message, yes_action, no_action):
    modal True

    frame:
        background "ui/yesno/bg.webp"

        xpadding 284
        ypadding 192

        text __(message):
            yoffset 50
            size 30
            xmaximum 680
            text_align 0.5
            xalign 0.5
            color "#24282d"

        imagebutton:
            idle "ui/yesno/yes.webp"
            hover "ui/yesno/yes_hover.webp"
            focus_mask True
            xoffset 455
            yoffset 181
            action yes_action

        imagebutton:
            idle "ui/yesno/no.webp"
            hover "ui/yesno/no_hover.webp"
            focus_mask True
            xoffset 588
            yoffset 180
            action no_action

screen yesno_saveload():
    frame:
        background "ui/saveload/prompt.webp"

        xpos 94
        ypos y

        text __("Are you sure you want to overwrite?"):
            xanchor 0.5
            xpos 236
            ypos 20
            xmaximum 472
            ymaximum 50
            color "#716957"

        imagebutton:
            idle "ui/saveload/no.webp"
            hover "ui/saveload/no_hover.webp"
            xanchor 0.5
            yanchor 0.5
            xpos 184
            ypos 84
            xmaximum 40
            ymaximum 40
            action Hide('yesno_saveload')

        imagebutton:
            idle "ui/saveload/yes.webp"
            hover "ui/saveload/yes_hover.webp"
            xanchor 0.5
            yanchor 0.5
            xpos 282
            ypos 84
            xmaximum 40
            ymaximum 40
            action [FileSave(i, confirm=False), Hide('yesno_saveload') ]





########################################################################################
# HUD elements.
########################################################################################

# Choice window.
screen choice(items):
    window:
        style "menu_window"
        background "ui/choicebar.webp"
        xalign 0.5
        yalign 0.5

        vbox:
            style "menu"
            xalign 0.5
            yoffset -2

            for caption, act, chosen in items:
                button:
                    action act
                    style "menu_choice_button"
                    text caption style "menu_choice"
                    xalign 0.5
                    yoffset 100
                    left_padding 30
                    bottom_padding 20

# The saybox.
screen say(what, who, double_speak=False):
    python:
        bg = None
        tb = Null()
        bg_base = 'ui/textbar/' + get_ui_season() + '/'
        tb_base = 'ui/textbar/names/' + GameContext.get_language() + '/'

        vinfo = store._get_voice_info()
        speaking = speaking_flavour = False

        if who:
            if not double_speak:
                if who in character_tags:
                    tag = character_tags[who]
                else:
                    for c in characters:
                        if characters[c] == who:
                            tag = c
                            break
                    else:
                        tag = who.lower()
                sprite_tag = tag.split('_', 1)[0]

                if vinfo.filename and vinfo.tag.rstrip('u') in (tag, sprite_tag):
                    voice_file = vinfo.filename.rsplit('/', 1)[1]
                    if voice_file.startswith('scene_') or voice_file[0].isdigit():
                        speaking = True
                    else:
                        speaking_flavour = True

                who = who.split('{', 1)[0]
            if double_speak:
                bg = bg_base + 'double.webp'
                tb = tb_base + '_'.join(who) + '.webp'
            elif bg_base + who.lower() + '.webp' in renpy.list_files():
                bg = bg_base + who.lower() + '.webp'
                tb = tb_base + who.lower() + '.webp'
            else:
                # Don't ask. Just don't.
                context = renpy.game.context()

                sprite = context.scene_lists.get_displayable_by_tag('master', sprite_tag)
                attributes = context.images.get_attributes('master', sprite_tag)
                phone = context.scene_lists.get_displayable_by_tag('screens', 'phone')

                if tb_base + tag + '.webp' in renpy.list_files():
                    tb = tb_base + tag + '.webp'

                if sprite is not None:
                    pos = renpy.get_placement(sprite)
                    xpos = (pos.xpos.relative if isinstance(pos.xpos, position) else
                            pos.xpos)
                    ypos = (pos.ypos.relative if isinstance(pos.ypos, position) else
                            pos.ypos)
                    
                    if xpos is not None and ypos is not None:
                        if ypos < 0.0 or ypos > 1.0:
                            bg = bg_base + 'default.webp'
                        elif xpos >= 0.80:
                            bg = bg_base + 'farright.webp'
                        elif xpos >= 0.70:
                            bg = bg_base + 'midright.webp'
                        elif xpos > 0.5:
                            bg = bg_base + 'right.webp'
                        elif xpos <= 0.20:
                            bg = bg_base + 'farleft.webp'
                        elif xpos <= 0.30:
                            bg = bg_base + 'midleft.webp'
                        elif xpos < 0.5:
                            bg = bg_base + 'left.webp'
                        elif 'flip' in attributes:
                            bg = bg_base + 'right.webp'
                        else:
                            bg = bg_base + 'left.webp'
                elif phone:
                    bg = bg_base + 'phone.webp'
        if not bg:
            bg = bg_base + 'default.webp'

        dialogue_color = {
            'fall':   '#352114',
            'winter': '#424351'
        }[get_ui_season()]
        if persistent.high_contrast:
            dialogue_color = "#000000"

        if persistent.font_mode == 'dyslexia':
            dialogue_font = "ui/OpenDyslexic3.ttf"
            dialogue_size = 18
            dialogue_yoffset = -15
            dialogue_spacing = 0
        elif persistent.font_mode == 'sans':
            dialogue_font = "ui/BalooTamma2-Medium.ttf"
            dialogue_size = 22
            dialogue_yoffset = -7
            dialogue_spacing = -5
        else:
            dialogue_font = "ui/SetFireToTheRain.ttf"
            dialogue_size = 22
            dialogue_yoffset = 0
            dialogue_spacing = 0

    window id "window":
        background bg
        yoffset 456

        frame:
            background Null()
            add tb:
                xpos 143
                ypos 28
            if speaking:
                add "ui/textbar/voice.webp":
                    xpos (160 + 11 * len(who))
                    ypos 0
            elif speaking_flavour:
                add "ui/textbar/voice-flavour.webp":
                    xpos (160 + 11 * len(who))
                    ypos 0

        frame:
            background Null()
            yminimum 262
            xpadding 135
            ypadding 15
            xmaximum 1100

            if double_speak:
                text what[0]:
                    id "what"
                    color dialogue_color
                    xpos 75
                    ypos 100
                    slow (not renpy.in_rollback())
                    font dialogue_font
                    size dialogue_size
                    yoffset dialogue_yoffset
                    line_spacing dialogue_spacing
                text what[1]:
                    id "what"
                    color dialogue_color
                    xpos 530
                    ypos 100
                    slow (not renpy.in_rollback())
                    font dialogue_font
                    size dialogue_size
                    yoffset dialogue_yoffset
                    line_spacing dialogue_spacing
            else:
                text what:
                    id "what"
                    color dialogue_color
                    xpos 75
                    ypos 100
                    font dialogue_font
                    size dialogue_size
                    yoffset dialogue_yoffset
                    line_spacing dialogue_spacing

# ugh
transform phone_anim:
    on show:
        yoffset config.screen_height
        ease 2.0 yoffset 0
    on hide:
        ease 2.0 yoffset config.screen_height

screen phone(mode, who=None, time=None, temperature=None):
    python:
        emoji = {
            '\\o/': __('yay'),
            ';)': __('wink'),
            ':>': __('smug'),
            ':)': __('smile'),
            '|(': __('sleepy'),
            ':(': __('sad'),
            '<3': __('heart'),
            ':s': __('confused'),
            'owo': __('blush'),
            '>:|': __('angry'),
            ':o': __('surprised'),
        }

    frame at phone_anim:
        background Null()
        xmaximum 580
        ymaximum 631
        yalign 1.0
        xalign 0.5

        # old save compatibility: phone may not have `waiting` attribute
        if getattr(phone, 'waiting', False):
            add "vfx/phone/ui-ctc-bg.webp":
                yalign 1.0
                yoffset 6
                xalign 0.5
                xoffset 25

            add "ctc":
                yalign 1.0
                yoffset 2
                xpos 494

        add "vfx/phone/bg.webp":
            xpos 50

        if mode == 'unlock':
            add "vfx/phone/ui-unlock.webp":
                xpos 60
                ypos 57
        elif mode == 'messages':
            add "vfx/phone/ui-msg.webp":
                xpos 66
                ypos 57

            $ messages = phone.messages.get(who, [])

            viewport id "phone_messages":
                xpos 90
                ypos 105
                yinitial 1.0
                xsize 390
                ysize 515

                vbox:
                    xsize 370
                    spacing -17

                    for i, (to, time, message) in enumerate(messages[-5:]):
                        python:
                            if to:
                                sn = 'self'
                            else:
                                sn = 'other'
                            if i < len(messages) - 1:
                                next_to, next_time, next_msg = messages[i + 1]
                                if to != next_to:
                                    sw = 'switch'
                                else:
                                    sw = 'cont'
                            else:
                                sw = 'fin'
                            box = 'vfx/phone/ui-msg-box-{}-{}.webp'.format(sn, sw)
                            ava = 'vfx/phone/ava' + ('-' + who if not to else '') + '.webp'
                            avaalign = 1.0 if to else 0.0
                            textoffset = (20, -85) if to else (95, -85)
                            textcolor = "#665f59" if to else "#ebe3d9"
                            textalign = 1.0 if to else 0.0
                            timecolor = "#a69a83" if to else "#b3a78d"
                            timeoffset = (3, 35) if to else (262, 40)
                            avaoffset = (5, -20) if to else (-5, -20)
                            alpha = 0.8 if to else -0.8

                            for txt, img in emoji.items():
                                message = message.replace(txt, '{image=vfx/phone/emoji/' + img + '.webp}')

                        frame:
                            background None
                            xsize 360
                            ysize 125
                            add box:
                                xalign 0.5
                                yalign 0.5
                            add ava at trotate(alpha):
                                xoffset avaoffset[0]
                                yoffset avaoffset[1]
                                #zoom 0.9
                                xalign avaalign
                            frame at trotate(alpha):
                                background None
                                xpos textoffset[0]
                                ypos textoffset[1]
                                xsize 230
                                text message at transparent(0.90):
                                    antialias False
                                    color textcolor
                                    font "ui/MerriweatherSans.ttf"
                                    size 18
                                    text_align textalign
                                    xalign textalign
                            frame:
                                background None
                                xpos timeoffset[0]
                                ypos timeoffset[1]
                                xsize 80
                                text time at trotate(alpha):
                                    color timecolor
                                    font "ui/MerriweatherSans.ttf"
                                    size 12
                                    text_align textalign
                                    xalign textalign

                    $ renpy.run(Scroll('phone_messages', 'vertical increase', 9999999999))
                    add "vfx/phone/ui-msg-buttons.webp":
                        xalign 0.5
                        xoffset -10
                        yoffset -14 # + (10 * i)

            if len(messages) > 4:
                add "vfx/phone/ui-msg-fade.webp":
                    xpos 75
                    ypos 105

        elif mode == 'call-in':
            add "vfx/phone/ui-call-in.webp":
                xpos 60
                ypos 57

        add "vfx/phone/statusbar.webp":
            xpos 67
            ypos 63
        add "vfx/phone/cracks.webp":
            xpos 67
            ypos 58

screen text_log():
    modal True
    zorder 99999

    key "K_ESCAPE" action Hide('text_log', dissolve)

    python:
        if persistent.font_mode == 'dyslexia':
            dialogue_font = "ui/OpenDyslexic3.ttf"
            dialogue_size = 18
            dialogue_yoffset = -5
        elif persistent.font_mode == 'sans':
            dialogue_font = "ui/BalooTamma2-Medium.ttf"
            dialogue_size = 18
            dialogue_yoffset = 0
        else:
            dialogue_font = "ui/SetFireToTheRain.ttf"
            dialogue_size = 22
            dialogue_yoffset = 0

    frame:
        background "ui/overlay.webp" at tdissolve(0.5)

        padding (90, 75)

        side "c r":
            yfill True

            viewport id "text_log_view":
                mousewheel True
                yinitial 1.0
                yalign 1.0

                vbox:
                    spacing 10
                    for (type, who, what) in store.text_log.all():
                        $ who = who or ''
                        python:
                            for char in characters:
                                if remove_text_tags(characters[char]) == who:
                                    break
                            else:
                                char = ''

                        if type == 'dialogue':
                            hbox:
                                spacing 12
                                label who:
                                    xsize 100
                                    xalign 1.0
                                    text_xalign 1.0
                                    text_color (characters.get(char.lower(), {'color': '#ffffff'})['color'])
                                    text_bold True
                                    text_outlines [(2, '#292d34', 0, 0)]
                                    yoffset -2
                                label what:
                                    text_font dialogue_font
                                    text_size dialogue_size
                                    yoffset dialogue_yoffset

            vbar value YScrollValue('text_log_view'):
                xpos 5
                ypos 35
                top_bar "ui/preferences/scrollbar.webp"
                bottom_bar "ui/preferences/scrollbar.webp"
                thumb "ui/preferences/scrollbar_handle.webp"
                ymaximum 493
                xmaximum 30
                top_gutter 10
                bottom_gutter 10

        textbutton _("Close"):
            xpos 880
            ypos 565
            background "ui/pause/history.webp"
            left_padding 85
            top_padding 10
            text_size 29
            text_color "#faf6e7"
            text_hover_outlines [(3, "#4b565f", 0, 0)]
            text_hover_xoffset -3
            text_hover_yoffset -3
            action Hide('text_log', dissolve)



image ctc = DynamicDisplayable(lambda st, at: (Animation(
    'ui/textbar/' + get_ui_season() + '/ctc1.webp', 0.5,
    'ui/textbar/' + get_ui_season() + '/ctc2.webp', 0.5
), None))

image ctc_letterbox = Animation(
    'ui/textbar/ctclb1.webp', 0.5,
    'ui/textbar/ctclb2.webp', 0.5
)

# CTC indicator.
init -50 python:
    def ctc(st, at):
        return At("ctc", ctc_transform), None

    def ctc_letterbox(st, at):
        return At("ctc_letterbox", ctc_transform), None

transform ctc_transform:
    xpos 1050
    ypos 666
    alpha 0.0
    linear 1.0 alpha 1.0

# Skip indicator.
screen skip_indicator():
    $ ind = lang_img('ui/hud/' + get_ui_season() + '/skip.webp')
    add ind at skipind_transform

transform skipind_transform:
    xanchor 0.0
    xpos 0
    ypos 0
    on show:
        yanchor 1.0
        ease 1.0 yanchor 0.0
    on hide:
        yanchor 0.0
        ease 1.0 yanchor 1.0

# Screenshot indicator.
screen screenshot_indicator():
    $ ind = lang_img('ui/hud/' + get_ui_season() + '/screenshot.webp')
    add ind at screenind_transform

transform screenind_transform:
    yanchor 1.0
    ypos 0
    xpos 120
    on show:
        ease 1.0 yanchor 0.0
    on hide:
        ease 1.0 yanchor 1.0
