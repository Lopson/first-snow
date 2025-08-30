init python:
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
        
        def is_locked(self) -> bool:
            if self.locked is None:
                return True
            
            if isinstance(self.locked, bool):
                if self.locked:
                    return True
                return False
            
            if callable(self.locked):
                return self.locked()

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
        file=['cg act1 balcony morning'],
        thumb=['cg act1 balcony morning thumb'],
        locked=lambda: not GameContext.scene_seen('1S1')
    ),

    GalleryItem(
        title=__('Art Matters'),
        file=['title act1'],
        thumb=['title act1 thumb'],
        locked=lambda: not GameContext.scene_seen('1S2')
    ),

    GalleryItem(
        title=__('The Painter'),
        file=['cg act1 eileenpainting'],
        thumb=['cg act1 eileenpainting thumb'],
        locked=lambda: not GameContext.scene_seen('1S5')
    ),

    GalleryItem(
        title=__('Cooking'),
        file=[
            'cg act1 cooking',
            'cg act1 cooking happy'
        ],
        thumb=[
            'cg act1 cooking thumb',
            'cg act1 cooking happy thumb'
        ],
        locked=lambda: not GameContext.scene_seen('1S6')
    ),

    GalleryItem(
        title=__('Toast!'),
        file=['cg act1 clubtoast'],
        thumb=['cg act1 clubtoast thumb'],
        locked=lambda: not GameContext.scene_seen('1S7')
    ),

    GalleryItem(
        title=__('Falling Snow'),
        file=['title act2'],
        thumb=['title act2 thumb'],
        locked=lambda: not GameContext.scene_seen('2S1')
    ),

    GalleryItem(
        title=__('Nude Painting'),
        file=(lambda:
            [
                'cg act2 boobpainting',
                'cg act2 boobpainting embarrassed',
                'cg act2 boobpainting smile'
            ] if GameContext.explicit_allowed() else [
                'cg act2 nudepainting',
                'cg act2 nudepainting embarrassed',
                'cg act2 nudepainting smile'
            ]
        ),
        thumb= (lambda:
            [
                'cg act2 boobpainting thumb',
                'cg act2 boobpainting embarrassed thumb',
                'cg act2 boobpainting smile thumb'
            ] if GameContext.explicit_allowed() else [
                'cg act2 nudepainting thumb',
                'cg act2 nudepainting embarrassed thumb',
                'cg act2 nudepainting smile thumb'
            ]
        ),
        locked=lambda: not GameContext.scene_seen('2S3')
    ),

    GalleryItem(
        title=__('Balcony Chat'),
        preview='cg act2 balconychat talk thumb',
        file=[
            'cg act2 balconychat alone',
            'cg act2 balconychat rose',
            'cg act2 balconychat talk',
            'cg act2 balconychat talk 2',
            'cg act2 balconychat talk 3',
            'cg act2 balconychat talk 4',
            'cg act2 balconychat talk 5'
        ],
        thumb=[
            'cg act2 balconychat alone thumb',
            'cg act2 balconychat rose thumb',
            'cg act2 balconychat talk thumb',
            'cg act2 balconychat talk 2 thumb',
            'cg act2 balconychat talk 3 thumb',
            'cg act2 balconychat talk 4 thumb',
            'cg act2 balconychat talk 5 thumb'
            ],
        locked=lambda: not GameContext.scene_seen('2S4')
    ),

    GalleryItem(
        title=__('Kiss'),
        file=[
            'cg act2 kiss surprise',
            'cg act2 kiss after'
        ],
        thumb=[
            'cg act2 kiss surprise thumb',
            'cg act2 kiss after thumb'
        ],
        locked=lambda: not GameContext.scene_seen('2S6')
    ),

    GalleryItem(
        title=__('Zoo'),
        file=[
            'cg act2 zoo smile',
            'cg act2 zoo bird'
        ],
        thumb=[
            'cg act2 zoo smile thumb',
            'cg act2 zoo bird thumb'
        ],
        locked=lambda: not GameContext.scene_seen('2S8')
    ),

    GalleryItem(
        title=__('Fingering'),
        file=[
            'cg act2 finger start',
            'cg act2 finger mid',
            'cg act2 finger end'
        ],
        thumb=[
            'cg act2 finger start thumb',
            'cg act2 finger mid thumb',
            'cg act2 finger end thumb'
        ],
        locked=lambda: not GameContext.scene_seen('2S8_b'),
        visible=lambda: GameContext.explicit_allowed(),
    ),

    GalleryItem(
        title=__('H'),
        file=[
            'cg act2 cunnilingus start',
            'cg act2 cunnilingus mid',
            'cg act2 cunnilingus end'
        ],
        thumb=[
            'cg act2 cunnilingus start thumb',
            'cg act2 cunnilingus mid thumb',
            'cg act2 cunnilingus end thumb'
        ],
        locked=lambda: not GameContext.scene_seen('2S8_b'),
        visible=lambda: GameContext.explicit_allowed(),
    ),

    GalleryItem(
        title=__('Pillowtalk'),
        file=[
            'cg act2 pillowtalk eyesclosed',
            'cg act2 pillowtalk talk'
        ],
        thumb=[
            'cg act2 pillowtalk eyesclosed thumb',
            'cg act2 pillowtalk talk thumb'
        ],
        locked=lambda: not GameContext.scene_seen('2S8_c')
    ),

    GalleryItem(
        title=__('Photo'),
        file=['cg act2 photo'],
        thumb=['cg act2 photo thumb'],
        locked=lambda: not GameContext.scene_seen('2S9')
    ),

    GalleryItem(
        title=__('A World Away'),
        file=['title act3'],
        thumb=['title act3 thumb'],
        locked=lambda: not GameContext.scene_seen('3S1')
    ),

    GalleryItem(
        title=__('Roadtrip'),
        file=['cg act3 roadtrip {}'.format(i) for i in range(1, 7)],
        thumb=['cg act3 roadtrip {} thumb'.format(i) for i in range(1, 7)],
        locked=lambda: not GameContext.scene_seen('3S1')
    ),

    GalleryItem(
        title=__('Family Dinner'),
        file=['cg act3 familydinner {}'.format(i) for i in range(1, 11)],
        thumb=['cg act3 familydinner {} thumb'.format(i) for i in range(1, 11)],
        locked=lambda: not GameContext.scene_seen('3S2')
    ),

    GalleryItem(
        title=__('Pinned!'),
        file=[
            'cg act3 pinned allisontalk',
            'cg act3 pinned eileentalk',
            'cg act3 pinned shocked',
            'cg act3 pinned kiss'
        ],
        thumb=[
            'cg act3 pinned allisontalk thumb',
            'cg act3 pinned eileentalk thumb',
            'cg act3 pinned shocked thumb',
            'cg act3 pinned kiss thumb'
        ],
        locked=lambda: not GameContext.scene_seen('3S2')
    ),

    GalleryItem(
        title=__('Kitchen'),
        file=['cg act3 kitchen'],
        thumb=['cg act3 kitchen thumb'],
        locked=lambda: not GameContext.scene_seen('3S3')
    ),

    GalleryItem(
        title=__('Unison'),
        file=['cg act3 mast{}'.format(i) for i in range(1, 8)],
        thumb=['cg act3 mast{} thumb'.format(i) for i in range(1, 8)],
        locked=lambda: not GameContext.scene_seen('3S3_b'),
        visible=lambda: GameContext.explicit_allowed(),
    ),

    GalleryItem(
        title=__('Snowmen'),
        file=['cg act3 snowmen'],
        thumb=['cg act3 snowmen thumb'],
        locked=lambda: not GameContext.scene_seen('3S3_c')
    ),

    GalleryItem(
        title=__('Overlook'),
        file=['cg act3 swings'],
        thumb=['cg act3 swings thumb'],
        locked=lambda: not GameContext.scene_seen('3S6')
    ),

    GalleryItem(
        title=__('Sleeping Sisters'),
        file=['cg act3 sleepingsisters'],
        thumb=['cg act3 sleepingsisters thumb'],
        locked=lambda: not GameContext.scene_seen('3S7')
    ),

    GalleryItem(
        title=__('Together'),
        file=[
            'cg act3 hug run',
            'cg act3 hug end'
        ],
        thumb=[
            'cg act3 hug run thumb',
            'cg act3 hug end thumb'
        ],
        locked=lambda: not GameContext.scene_seen('3S8')
    ),

    GalleryItem(
        title=__('Voiced'),
        file=['cg act4 vacg{}'.format(i)for i in range(1, 5)],
        thumb=['cg act4 vacg{} thumb'.format(i)for i in range(1, 5)],
        locked=lambda: not GameContext.scene_seen('4S2')
    )
]

define guest_art = [
    GalleryItem(
        author='Szmitten',
        url='https://x.com/szmitten',
        file=['cg guest szmitten'],
        thumb=['cg guest szmitten thumb'],
        native=['cg guest szmitten native']
    ),

    GalleryItem(
        author='Lilium',
        file=['cg guest lilium'],
        thumb=['cg guest lilium thumb'],
        native=['cg guest lilium native']
    ),

    GalleryItem(
        author='adirosa',
        url='https://x.com/adirosette',
        file=['cg guest adirosa'],
        thumb=['cg guest adirosa thumb'],
        native=['cg guest adirosa native']
    ),

    GalleryItem(
        author='Anon',
        file=['cg guest anon'],
        thumb=['cg guest anon thumb'],
        native=['cg guest anon native']
    ),
    
    GalleryItem(
        author='VCR',
        url='https://x.com/Hachisame',
        file=['cg guest vcr'],
        thumb=['cg guest vcr thumb'],
        native=['cg guest vcr native']
    ),
    
    GalleryItem(
        author='rtil',
        url='https://x.com/rtil',
        file=['cg guest rtil'],
        thumb=['cg guest rtil thumb'],
        native=['cg guest rtil native']
    ),
    
    GalleryItem(
        author='umujacha',
        url='https://x.com/umujacha',
        file=['cg guest umujacha'],
        thumb=['cg guest umujacha thumb'],
        native=['cg guest umujacha native']
    ),

    GalleryItem(
        author='minute',
        url='https://x.com/theominute',
        file=['cg guest minute'],
        thumb=['cg guest minute thumb'],
        native=['cg guest minute native']
    ),
    
    GalleryItem(
        author='TopHat',
        url='https://x.com/ToppeHatte',
        file=['cg guest tophat'],
        thumb=['cg guest tophat thumb'],
        native=['cg guest tophat native']
    ),

    GalleryItem(
        author='AcoTan',
        url='https://x.com/AcoTan2194',
        file=['cg guest acotan'],
        thumb=['cg guest acotan thumb'],
        native=['cg guest acotan native']
    ),

    GalleryItem(
        author='Skrats',
        url='https://x.com/Skratsu',
        file=['cg guest skrats'],
        thumb=['cg guest skrats thumb'],
        native=['cg guest skrats native']
    ),

    GalleryItem(
        author='tentakl',
        file=[
            Animation(
                'cg guest tentakl 1',
                0.5,
                'cg guest tentakl 2',
                0.5
            )
        ],
        thumb=['cg guest tentakl thumb'],
    ),

    GalleryItem(
        author='Chiru',
        url='https://x.com/guy_kun',
        file=['cg guest chiru'],
        thumb=['cg guest chiru thumb'],
        native=['cg guest chiru native']
    ),

    GalleryItem(
        author='renessia',
        file=['cg guest renessia'],
        thumb=['cg guest renessia thumb'],
        native=['cg guest renessia native']
    ),

    GalleryItem(
        author='Anna',
        url='https://x.com/ripandtir',
        file=['cg guest anna'],
        thumb=['cg guest anna thumb'],
        native=['cg guest anna native']
    ),

    GalleryItem(
        author='Cura & tentakl',
        url='https://x.com/cura_chan',
        file=['cg guest cura tentakl'],
        thumb=['cg guest cura tentakl thumb'],
        native=['cg guest cura tentakl native']
    ),

    GalleryItem(
        author='All-Maker',
        url='https://x.com/AllMaker',
        file=['cg guest all-maker'],
        thumb=['cg guest all-maker thumb'],
        native=['cg guest all-maker native']
    )
]
