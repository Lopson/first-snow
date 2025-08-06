init python:
    _constant = True

    from dataclasses import dataclass
    from typing import Callable

    @dataclass
    class GalleryItem:
        file: list[str]
        thumb: list[str] | Callable
        title: str | None = None
        locked: bool | Callable | None = None
        visible: bool | Callable | None = None
        native: list[str] | None = None
        preview: str | None = None
        author: str | None = None
        url: str | None = None

        def is_visible(self) -> bool:
            if self.visible is None:
                return True
            
            if isinstance(self.visible, bool):
                if self.visible:
                    return True
                return False
            
            if callable(self.visible):
                return self.visible()

        def eval_piece(self) -> None:
            if callable(self.file):
                self.file = self.file()
            if callable(self.thumb):
                self.thumb = self.thumb()
            if callable(self.locked):
                self.locked = self.locked()
            if callable(self.visible):
                self.visible = self.visible()


define cg_art = [
    GalleryItem(
        title=__('Balcony'),
        file=['cgs/act1_balcony_morning.webp'],
        thumb=['cgs/act1_balcony_morning_thumb.webp'],
        locked=lambda: not game_context.scene_seen('1S1')
    ),

    GalleryItem(
        title=__('Art Matters'),
        file=['vfx/title/act1.webp'],
        thumb=['vfx/title/act1_thumb.webp'],
        locked=lambda: not game_context.scene_seen('1S2')
    ),

    GalleryItem(
        title=__('The Painter'),
        file=['cgs/act1_eileenpainting.webp'],
        thumb=['cgs/act1_eileenpainting_thumb.webp'],
        locked=lambda: not game_context.scene_seen('1S5')
    ),

    GalleryItem(
        title=__('Cooking'),
        file=['cgs/act1_cooking.webp', 'cgs/act1_cooking_happy.webp'],
        thumb=['cgs/act1_cooking_thumb.webp', 'cgs/act1_cooking_happy_thumb.webp'],
        locked=lambda: not game_context.scene_seen('1S6')
    ),

    GalleryItem(
        title=__('Toast!'),
        file=['cgs/act1_clubtoast.webp'],
        thumb=['cgs/act1_clubtoast_thumb.webp'],
        locked=lambda: not game_context.scene_seen('1S7')
    ),

    GalleryItem(
        title=__('Falling Snow'),
        file=['vfx/title/act2.webp'],
        thumb=['vfx/title/act2_thumb.webp'],
        locked=lambda: not game_context.scene_seen('2S1')
    ),

    GalleryItem(
        title=__('Nude Painting'),
        file=(lambda:
            [
                'dlc/h/cgs/act2_boobpainting.webp',
                'dlc/h/cgs/act2_boobpainting_embarrassed.webp',
                'dlc/h/cgs/act2_boobpainting_smile.webp'
            ] if game_context.explicit_allowed() else [
                'cgs/act2_nudepainting.webp',
                'cgs/act2_nudepainting_embarrassed.webp',
                'cgs/act2_nudepainting_smile.webp'
            ]
        ),
        thumb= (lambda:
            [
                'dlc/h/cgs/act2_boobpainting_thumb.webp',
                'dlc/h/cgs/act2_boobpainting_embarrassed_thumb.webp',
                'dlc/h/cgs/act2_boobpainting_smile_thumb.webp'
            ] if game_context.explicit_allowed() else [
                'cgs/act2_nudepainting_thumb.webp',
                'cgs/act2_nudepainting_embarrassed_thumb.webp',
                'cgs/act2_nudepainting_smile_thumb.webp'
            ]
        ),
        locked=lambda: not game_context.scene_seen('2S3')
    ),

    GalleryItem(
        title=__('Balcony Chat'),
        preview='cgs/act2_balconychat_talk_thumb.webp',
        file=[
            'cgs/act2_balconychat_alone.webp',
            'cgs/act2_balconychat_rose.webp',
            'cgs/act2_balconychat_talk.webp',
            'cgs/act2_balconychat_talk_2.webp',
            'cgs/act2_balconychat_talk_3.webp',
            'cgs/act2_balconychat_talk_4.webp',
            'cgs/act2_balconychat_talk_5.webp'
        ],
        thumb=[
            'cgs/act2_balconychat_alone_thumb.webp',
            'cgs/act2_balconychat_rose_thumb.webp',
            'cgs/act2_balconychat_talk_thumb.webp',
            'cgs/act2_balconychat_talk_2_thumb.webp',
            'cgs/act2_balconychat_talk_3_thumb.webp',
            'cgs/act2_balconychat_talk_4_thumb.webp',
            'cgs/act2_balconychat_talk_5_thumb.webp'
            ],
        locked=lambda: not game_context.scene_seen('2S4')
    ),

    GalleryItem(
        title=__('Kiss'),
        file=['cgs/act2_kiss_surprise.webp', 'cgs/act2_kiss_after.webp'],
        thumb=['cgs/act2_kiss_surprise_thumb.webp', 'cgs/act2_kiss_after_thumb.webp'],
        locked=lambda: not game_context.scene_seen('2S6')
    ),

    GalleryItem(
        title=__('Zoo'),
        file=['cgs/act2_zoo_smile.webp', 'cgs/act2_zoo_bird.webp'],
        thumb=['cgs/act2_zoo_smile_thumb.webp', 'cgs/act2_zoo_bird_thumb.webp'],
        locked=lambda: not game_context.scene_seen('2S8')
    ),

    GalleryItem(
        title=__('Fingering'),
        file=[
            'dlc/h/cgs/act2_finger_start.webp',
            'dlc/h/cgs/act2_finger_mid.webp',
            'dlc/h/cgs/act2_finger_end.webp'
        ],
        thumb=[
            'dlc/h/cgs/act2_finger_start_thumb.webp',
            'dlc/h/cgs/act2_finger_mid_thumb.webp',
            'dlc/h/cgs/act2_finger_end_thumb.webp'
        ],
        locked=lambda: not game_context.scene_seen('2S8_b'),
        visible=lambda: game_context.explicit_allowed(),
    ),

    GalleryItem(
        title=__('H'),
        file=[
            'dlc/h/cgs/act2_cunnilingus_start.webp',
            'dlc/h/cgs/act2_cunnilingus_mid.webp',
            'dlc/h/cgs/act2_cunnilingus_end.webp'
        ],
        thumb=[
            'dlc/h/cgs/act2_cunnilingus_start_thumb.webp',
            'dlc/h/cgs/act2_cunnilingus_mid_thumb.webp',
            'dlc/h/cgs/act2_cunnilingus_end_thumb.webp'
        ],
        locked=lambda: not game_context.scene_seen('2S8_b'),
        visible=lambda: game_context.explicit_allowed(),
    ),

    GalleryItem(
        title=__('Pillowtalk'),
        file=[
            'cgs/act2_pillowtalk_eyesclosed.webp',
            'cgs/act2_pillowtalk_talk.webp'
        ],
        thumb=[
            'cgs/act2_pillowtalk_eyesclosed_thumb.webp',
            'cgs/act2_pillowtalk_talk_thumb.webp'
        ],
        locked=lambda: not game_context.scene_seen('2S8_c')
    ),

    GalleryItem(
        title=__('Photo'),
        file=['cgs/act2_photo.webp'],
        thumb=['cgs/act2_photo_thumb.webp'],
        locked=lambda: not game_context.scene_seen('2S9')
    ),

    GalleryItem(
        title=__('A World Away'),
        file=['vfx/title/act3.webp'],
        thumb=['vfx/title/act3_thumb.webp'],
        locked=lambda: not game_context.scene_seen('3S1')
    ),

    GalleryItem(
        title=__('Roadtrip'),
        file=['cgs/act3_roadtrip_{}.webp'.format(i) for i in range(1, 7)],
        thumb=['cgs/act3_roadtrip_{}_thumb.webp'.format(i) for i in range(1, 7)],
        locked=lambda: not game_context.scene_seen('3S1')
    ),

    GalleryItem(
        title=__('Family Dinner'),
        file=['cgs/act3_familydinner_{}.webp'.format(i) for i in range(1, 11)],
        thumb=['cgs/act3_familydinner_{}_thumb.webp'.format(i) for i in range(1, 11)],
        locked=lambda: not game_context.scene_seen('3S2')
    ),

    GalleryItem(
        title=__('Pinned!'),
        file=[
            'cgs/act3_pinned_allisontalk.webp',
            'cgs/act3_pinned_eileentalk.webp',
            'cgs/act3_pinned_shocked.webp',
            'cgs/act3_pinned_kiss.webp'
        ],
        thumb=[
            'cgs/act3_pinned_allisontalk_thumb.webp',
            'cgs/act3_pinned_eileentalk_thumb.webp',
            'cgs/act3_pinned_shocked_thumb.webp',
            'cgs/act3_pinned_kiss_thumb.webp'
        ],
        locked=lambda: not game_context.scene_seen('3S2')
    ),

    GalleryItem(
        title=__('Kitchen'),
        file=['cgs/act3_kitchen.webp'],
        thumb=['cgs/act3_kitchen_thumb.webp'],
        locked=lambda: not game_context.scene_seen('3S3_a')
    ),

    GalleryItem(
        title=__('Unison'),
        file=['dlc/h/cgs/act3_mast{}.webp'.format(i) for i in range(1, 8)],
        thumb=['dlc/h/cgs/act3_mast{}_thumb.webp'.format(i) for i in range(1, 8)],
        locked=lambda: not game_context.scene_seen('3S3_b'),
        visible=lambda: game_context.explicit_allowed(),
    ),

    GalleryItem(
        title=__('Snowmen'),
        file=['cgs/act3_snowmen.webp'],
        thumb=['cgs/act3_snowmen_thumb.webp'],
        locked=lambda: not game_context.scene_seen('3S3_c')
    ),

    GalleryItem(
        title=__('Overlook'),
        file=['cgs/act3_swings.webp'],
        thumb=['cgs/act3_swings_thumb.webp'],
        locked=lambda: not game_context.scene_seen('3S6')
    ),

    GalleryItem(
        title=__('Sleeping Sisters'),
        file=['cgs/act3_sleepingsisters.webp'],
        thumb=['cgs/act3_sleepingsisters_thumb.webp'],
        locked=lambda: not game_context.scene_seen('3S7')
    ),

    GalleryItem(
        title=__('Together'),
        file=['cgs/act3_hug_run.webp', 'cgs/act3_hug_end.webp'],
        thumb=['cgs/act3_hug_run_thumb.webp', 'cgs/act3_hug_end_thumb.webp'],
        locked=lambda: not game_context.scene_seen('3S8')
    ),

    GalleryItem(
        title=__('Voiced'),
        file=['cgs/act4_vacg{}.webp'.format(i)for i in range(1, 5)],
        thumb=['cgs/act4_vacg{}_thumb.webp'.format(i)for i in range(1, 5)],
        locked=lambda: not game_context.scene_seen('4S2')
    )
]

define guest_art = [
    GalleryItem(
        author='Szmitten',
        url='https://x.com/szmitten',
        file=['cgs/guest/szmitten.webp'],
        thumb=['cgs/guest/szmitten_thumb.webp'],
        native=['cgs/guest/szmitten_native.webp']
    ),

    GalleryItem(
        author='Lilium',
        file=['cgs/guest/lilium.webp'],
        thumb=['cgs/guest/lilium_thumb.webp'],
        native=['cgs/guest/lilium_native.webp']
    ),

    GalleryItem(
        author='adirosa',
        url='https://x.com/adirosette',
        file=['cgs/guest/adirosa.webp'],
        thumb=['cgs/guest/adirosa_thumb.webp'],
        native=['cgs/guest/adirosa_native.webp']
    ),

    GalleryItem(
        author='Anon',
        file=['cgs/guest/anon.webp'],
        thumb=['cgs/guest/anon_thumb.webp'],
        native=['cgs/guest/anon_native.webp']
    ),
    
    GalleryItem(
        author='VCR',
        url='https://x.com/Hachisame',
        file=['cgs/guest/vcr.webp'],
        thumb=['cgs/guest/vcr_thumb.webp'],
        native=['cgs/guest/vcr_native.webp']
    ),
    
    GalleryItem(
        author='rtil',
        url='https://x.com/rtil',
        file=['cgs/guest/rtil.webp'],
        thumb=['cgs/guest/rtil_thumb.webp'],
        native=['cgs/guest/rtil_native.webp']
    ),
    
    GalleryItem(
        author='umujacha',
        url='https://x.com/umujacha',
        file=['cgs/guest/umujacha.jpg'],
        thumb=['cgs/guest/umujacha_thumb.jpg'],
        native=['cgs/guest/umujacha_native.jpg']
    ),

    GalleryItem(
        author='minute',
        url='https://x.com/theominute',
        file=['cgs/guest/minute.jpg'],
        thumb=['cgs/guest/minute_thumb.jpg'],
        native=['cgs/guest/minute_native.jpg']
    ),
    
    GalleryItem(
        author='TopHat',
        url='https://x.com/ToppeHatte',
        file=['cgs/guest/tophat.webp'],
        thumb=['cgs/guest/tophat_thumb.webp'],
        native=['cgs/guest/tophat_native.webp']
    ),

    GalleryItem(
        author='AcoTan',
        url='https://x.com/AcoTan2194',
        file=['cgs/guest/acotan.webp'],
        thumb=['cgs/guest/acotan_thumb.webp'],
        native=['cgs/guest/acotan_native.webp']
    ),

    GalleryItem(
        author='Skrats',
        url='https://x.com/Skratsu',
        file=['cgs/guest/skrats.webp'],
        thumb=['cgs/guest/skrats_thumb.webp'],
        native=['cgs/guest/skrats_native.webp']
    ),

    GalleryItem(
        author='tentakl',
        file=[
            Animation(
                'cgs/guest/tentakl-1.webp',
                0.5,
                'cgs/guest/tentakl-2.webp',
                0.5
            )
        ],
        thumb=['cgs/guest/tentakl_thumb.webp'],
    ),

    GalleryItem(
        author='Chiru',
        url='https://x.com/guy_kun',
        file=['cgs/guest/chiru.webp'],
        thumb=['cgs/guest/chiru_thumb.webp'],
        native=['cgs/guest/chiru_native.webp']
    ),

    GalleryItem(
        author='renessia',
        file=['cgs/guest/renessia.webp'],
        thumb=['cgs/guest/renessia_thumb.webp'],
        native=['cgs/guest/renessia_native.webp']
    ),

    GalleryItem(
        author='Anna',
        url='https://x.com/ripandtir',
        file=['cgs/guest/anna.webp'],
        thumb=['cgs/guest/anna_thumb.webp'],
        native=['cgs/guest/anna_native.webp']
    ),

    GalleryItem(
        author='Cura & tentakl',
        url='https://x.com/cura_chan',
        file=['cgs/guest/cura__tentakl.webp'],
        thumb=['cgs/guest/cura__tentakl_thumb.webp'],
        native=['cgs/guest/cura__tentakl_native.webp']
    ),

    GalleryItem(
        author='All-Maker',
        url='https://x.com/AllMaker',
        file=['cgs/guest/all-maker.webp'],
        thumb=['cgs/guest/all-maker_thumb.webp'],
        native=['cgs/guest/all-maker_native.webp']
    )
]
