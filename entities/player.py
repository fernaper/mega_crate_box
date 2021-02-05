import arcade
import random

from entities.scene_object import SceneEntity
from colliders.collider import CircleCollider
from utilities.animations import AnimatedWalkingSprite


class Player(SceneEntity):

    # Physics
    MOVEMENT_SPEED = 8
    JUMP_SPEED = 28
    GRAVITY = 1.1

    def __init__(self, *args, radius: float=50, **kwargs) -> None:
        self.radius = radius
        self.color = random.choice([
            arcade.color.WILD_BLUE_YONDER,
            arcade.color.WINE,
            arcade.color.ZAFFRE,
            arcade.color.YALE_BLUE,
        ])

        collider = CircleCollider(self, self.radius)

        super().__init__(*args, collider=collider, **kwargs)


    def setup(self) -> None:
        self.sprite_list = arcade.SpriteList()
        self.animation = AnimatedWalkingSprite(8, center_x=self.x, center_y=self.y, animations_per_second=10)
        self.animation.stand_left_textures

        self.textures_idle_right = [
            arcade.load_texture('resources/sprites/player/idle.png', x=i*9, y=0, width=9, height=10)
            for i in range(5)
        ]

        self.textures_idle_left = [
            arcade.load_texture('resources/sprites/player/idle.png', x=i*9, y=0, width=9, height=10, mirrored=True)
            for i in range(5)
        ]

        self.textures_walking_right = [
            arcade.load_texture('resources/sprites/player/walking.png', x=i*9, y=0, width=9, height=10)
            for i in range(5)
        ]

        self.textures_walking_left = [
            arcade.load_texture('resources/sprites/player/walking.png', x=i*9, y=0, width=9, height=10, mirrored=True)
            for i in range(5)
        ]

        self.textures_jumping_right = [
            arcade.load_texture('resources/sprites/player/jumping.png', x=i*9, y=0, width=9, height=10)
            for i in range(3)
        ]

        self.textures_jumping_left = [
            arcade.load_texture('resources/sprites/player/jumping.png', x=i*9, y=0, width=9, height=10, mirrored=True)
            for i in range(3)
        ]

        self.animation.stand_right_textures = self.textures_idle_right
        self.animation.stand_left_textures = self.textures_idle_left
        self.animation.walk_right_textures = self.textures_walking_right
        self.animation.walk_left_textures = self.textures_walking_left
        self.animation.jumping_right_textures = self.textures_jumping_right
        self.animation.jumping_left_textures = self.textures_jumping_left

        self.sprite_list.append(self.animation)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.animation, arcade.SpriteList(),
            gravity_constant=Player.GRAVITY
        )

        super().setup()


    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == self.window.get_control('up'):
            self.animation.change_y = 15

        elif key == self.window.get_control('down'):
            self.animation.change_y = -15

        elif key == self.window.get_control('left'):
            self.animation.change_x = -15

        elif key == self.window.get_control('right'):
            self.animation.change_x = 15


    def on_key_release(self, key: int, modifiers: int) -> None:
        if key in (self.window.get_control('up'), self.window.get_control('down')):
            self.animation.change_y = 0
        elif key in (self.window.get_control('left'), self.window.get_control('right')):
            self.animation.change_x = 0


    def __str__(self) -> str:
        return f'<Player{super().__str__()[7:]}'