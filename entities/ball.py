import arcade
import random

from typing import List, TYPE_CHECKING

from colliders.collider import CircleCollider
from entities.scene_object import SceneEntity

if TYPE_CHECKING:
    from behaviours.behaviour import Behaviour


class Ball(SceneEntity):

    def __init__(self, *args, behaviours: 'List[Behaviour]'=[],
                 radius: float=50, **kwargs) -> None:
        self.radius = radius
        self.color = random.choice([
            arcade.color.WILD_BLUE_YONDER,
            arcade.color.WINE,
            arcade.color.ZAFFRE,
            arcade.color.YALE_BLUE,
        ])

        collider = CircleCollider(self, self.radius)

        super().__init__(*args, behaviours=behaviours, collider=collider)


    def on_draw(self) -> None:
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        super().on_draw()


    def __str__(self) -> str:
        return f'<Ball{super().__str__()[7:]}'
