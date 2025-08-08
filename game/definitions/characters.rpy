init python:
    from collections import namedtuple

    CharacterDetails = namedtuple("CharacterDetails", ["name", "properties"])

define characters = {
    # Main
    'allison':   CharacterDetails(__('Allison'), {'color': '#eef0f1'}),
    'eileen':    CharacterDetails(__('Eileen'), {'color': '#9a9065'}),
    'eileenu':   CharacterDetails(__('Mad girl{=eileen}'), {'color': '#9a9065'}),
    
    # Side
    'caprice':   CharacterDetails(__('Caprice'), {'color': '#6e9aa1'}),
    'millie':    CharacterDetails(__('Millie'), {'color': '#ba5a4d'}),
    'wallace':   CharacterDetails(__('Wallace'), {'color': '#b2678a'}),
    'wallaceu':  CharacterDetails(__('Tall guy{=wallace}'), {'color': '#b2678a'}),
    'rose':      CharacterDetails(__('Rose'), {'color': '#c7633b'}),
    'eve':       CharacterDetails(__('Eve'), {'color': '#f5ecc1'}),
    'dad':       CharacterDetails(__('Dad'), {'color': '#eef0f1'}),
    'andrew':    CharacterDetails(__('Andrew'), {'color': '#eef0f1'}),
    'elizabeth': CharacterDetails(__('Elizabeth'), {'color': '#eef0f1'}),
    'hayley':    CharacterDetails(__('Hayley'), {'color': '#9a9065'}),
    
    # Misc
    'everyone':  CharacterDetails(__('Everyone'), {'color': '#ffff00'}),
    'letterbox': CharacterDetails(
        "",
        {
            'color': '#ffffff', 'what_color': '#ffffff',
            'window_background': 'ui/textbar/empty.webp',
            'ctc': DynamicDisplayable(ctc_letterbox)
        }
    ),
    'eileenlb':  CharacterDetails(
        __('Eileen'),
        {
            'color': '#9a9065', 'what_color': '#ffffff',
            'window_background': 'ui/textbar/empty.webp',
            'ctc': DynamicDisplayable(ctc_letterbox)
        }
    )
}

define character_tags = {
    __('Mad girl{=eileen}'):  'eileen_madgirl',
    __('Tall guy{=wallace}'): 'wallace_tallguy'
}

init 1 python:
    # Define characters based on the contents of the `characters` dictionary.
    for character, details in characters.items():
        # NOTE `globals()` is a built-in Python function.    
        globals()[character] = Character(
            details.name, image=character, voice_tag=character, **details.properties
        )
