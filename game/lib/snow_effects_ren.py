"""renpy
init -1 python:
"""

# Screen and snow effects
from math import sin, cos, pi
from random import random, uniform, randint, choice
from typing import Callable, TYPE_CHECKING
from renpy.display.layout import Composite, MultiBox
from renpy.display.particle import SpriteManager, Sprite
from renpy.display.transform import Transform
from renpy.easy import displayable
if TYPE_CHECKING:
    from renpy import config


class SpriteLayer(object):
    def __init__(self,
                 child,
                 prefill: bool = False,
                 spawn_tries: int = 3,
                 spawn_rate: float = 0.02,
                 xmargin: float = 0.05 * config.screen_width,
                 ymargin: float = 0.08 * config.screen_height) -> None:
        super(SpriteLayer, self).__init__()

        self.manager: SpriteManager = SpriteManager(update=self.update)
        self.child = displayable(child)
        self.flakes: list[Sprite] = []
        self.spawn_tries: int = spawn_tries
        self.spawn_rate: float = spawn_rate
        self.xmargin: Callable = self.to_concrete(xmargin)
        self.ymargin: Callable = self.to_concrete(ymargin)

        if prefill:
            for _ in range(config.screen_height):
                if random() < self.spawn_rate:
                    self.flakes.append(self.spawn_flake(prefill=True))

    def to_concrete(self,
                    x: int | float | tuple[int | float | Callable, *tuple[int | float, ...]]
                    ) -> Callable:
        """
        This method returns a list of callables that will convert a given value
        `x` to a value that a SpriteLayer sub-class needs in order to work.

        @param x: A value or a tuple of variable length that either starts with a
        callable and is then filled with just numbers or is just made up of numbers.
        @return: A callable that converts the argument to its desired value.
        """
        if isinstance(x, tuple):
            # NOTE Errors are being suppressed here because the check for callable
            # should be enough to avoid any typing issues.
            if callable(x[0]):
                args: list[Callable] = [self.to_concrete(a) for a in x[1:]]
                return lambda f: x[0](f, *[a(f) for a in args]) # pyright: ignore[reportCallIssue]
            else:
                return lambda _: uniform(*x) # pyright: ignore[reportArgumentType]
        return lambda _: x

    def update(self, _) -> int:
        # Update existing flakes and destroy those that are no longer on screen.
        self.flakes[:] = [
            flake for flake in self.flakes if self.update_flake(flake)]

        # Create new flakes if desired.
        for _ in range(self.spawn_tries):
            if random() < self.spawn_rate:
                self.flakes.append(self.spawn_flake())

        return 0

    def spawn_flake(self, prefill: bool = True) -> Sprite:
        return self.manager.create(self.child)

    def update_flake(self, flake: Sprite) -> bool:
        """
        Destroys a flake if it's off-screen.
        
        @return: `False` if the flake has been destroyed; `True` otherwise.
        """

        if (flake.x < -self.xmargin(flake) or
                flake.x > config.screen_width + self.xmargin(flake)):
            flake.destroy()
            return False
        if (flake.y < -self.ymargin(flake) or
                flake.y > config.screen_height + self.ymargin(flake)):
            flake.destroy()
            return False
        return True


class SnowLayer(SpriteLayer):
    def __init__(self, *args, **kwargs):
        self.dir_rate = self.to_concrete(
            kwargs.pop('dir_rate', 0.005))
        self.xspeed = self.to_concrete(
            kwargs.pop('xspeed', (0, 0.0005 * config.screen_width)))
        self.xmult = self.to_concrete(
            kwargs.pop('xmult', 1))
        self.xvar = self.to_concrete(
            kwargs.pop('xvar', (0, 0.0002 * config.screen_width)))
        self.yspeed = self.to_concrete(
            kwargs.pop('yspeed', 0.0015 * config.screen_height))
        self.ymult = self.to_concrete(
            kwargs.pop('ymult', 1))
        self.yvar = self.to_concrete(
            kwargs.pop('yvar', (0, 0.0002 * config.screen_width)))

        super(SnowLayer, self).__init__(*args, **kwargs)

    def spawn_flake(self, prefill: bool = False) -> Sprite:
        if prefill:
            yinit = uniform(
                -self.ymargin(None),
                config.screen_height + self.ymargin(None)
            )
        else:
            yinit = -50

        flake = super(SnowLayer, self).spawn_flake(prefill)
        
        # NOTE These setattr assignments are used because the original code
        # doesn't sub-class `Sprite` in order to add these attributes. This
        # is then the only "legal" way to address this. Undoing that is
        # complicated as we're relying on a `super()` call to self to create
        # the snowflake sprite.
        flake.x = randint(0, config.screen_width)
        setattr(flake, "xinit", flake.x)
        setattr(flake, "xdir", choice([1, -1]))
        setattr(flake, "xmult", self.xmult(flake))
        flake.y = yinit
        setattr(flake, "ymult", self.ymult(flake))
        
        return flake

    def update_flake(self, flake: Sprite):
        setattr(flake, "xdir", getattr(flake, "xdir") * - \
            1 if self.dir_rate(None) and random() < self.dir_rate(None) else 1)
        flake.x += (self.xspeed(flake) * getattr(flake, "xmult") +
                    self.xvar(flake)) * getattr(flake, "xdir")
        flake.y += self.yspeed(flake) * getattr(flake, "ymult") + self.yvar(flake)
        return super(SnowLayer, self).update_flake(flake)


def flake_sin(flake: Sprite, period: int | float) -> float:
    return (sin((flake.y / float(period)) * 2 * pi) -
            (flake.x - getattr(flake, "xinit")) / getattr(flake, "xmult"))


def LightSnow(prefill: bool = False) -> MultiBox:
    """
    Gives us a white-colored snowfall.
    
    @return: a displayable that renders the snowfall.
    """

    return Composite(
        (config.screen_width, config.screen_height),
        (0, 0), SnowLayer(
            "vfx/smallflake.webp", prefill=prefill, spawn_rate=0.10,
            xspeed=(flake_sin, 100), xmult=5,  xvar=0, ymult=0.5, dir_rate=0).manager,
        (0, 0), SnowLayer(
            "vfx/medflake.webp", prefill=prefill, spawn_rate=0.04,
            xspeed=(flake_sin, 200), xmult=20, xvar=0, ymult=0.7, dir_rate=0).manager,
        (0, 0), SnowLayer(
            "vfx/bigflake.webp", prefill=prefill, spawn_rate=0.02,
            xspeed=(flake_sin, 500), xmult=60, xvar=0, dir_rate=0).manager)


def LightSnowSepia(prefill: bool = False) -> MultiBox:
    """
    Gives us a sepia-tinted white-colored snowfall.
    
    @return: a displayable that renders the snowfall.
    """

    return Composite(
        (config.screen_width, config.screen_height),
        (0, 0), SnowLayer(
            Transform("vfx/smallflake.webp", matrixcolor=SepiaMatrix()), # pyright: ignore[reportUndefinedVariable]
            prefill=prefill, spawn_rate=0.10, xspeed=(flake_sin, 100), xmult=5,
            xvar=0, ymult=0.5, dir_rate=0).manager,
        (0, 0), SnowLayer(
            Transform("vfx/medflake.webp", matrixcolor=SepiaMatrix()), # pyright: ignore[reportUndefinedVariable]
            prefill=prefill, spawn_rate=0.04, xspeed=(flake_sin, 200), xmult=20,
            xvar=0, ymult=0.7, dir_rate=0).manager,
        (0, 0), SnowLayer(
            Transform("vfx/bigflake.webp", matrixcolor=SepiaMatrix()), # pyright: ignore[reportUndefinedVariable]
            prefill=prefill, spawn_rate=0.02, xspeed=(flake_sin, 500), xmult=60,
            xvar=0, dir_rate=0).manager
    )
