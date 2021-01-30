import arcade
import random

from entities.scene_object import SceneEntity
from colliders.collider import CircleCollider


class Player(SceneEntity):

    def __init__(self, *args, behaviours=[], radius=50):
        self.radius = radius
        self.color = random.choice([
            arcade.color.WILD_BLUE_YONDER,
            arcade.color.WINE,
            arcade.color.ZAFFRE,
            arcade.color.YALE_BLUE,
        ])

        collider = CircleCollider(self, self.radius)

        super().__init__(*args, behaviours=behaviours, collider=collider)


    def on_draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        super().on_draw()


    def __str__(self):
        return f'<Player{super().__str__()[7:]}'
