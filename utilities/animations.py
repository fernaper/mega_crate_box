import math

from arcade import Sprite

from typing import List


FACE_RIGHT = 1
FACE_LEFT = 2
FACE_UP = 3
FACE_DOWN = 4


class AnimatedWalkingSprite(Sprite):
    """
    Sprite for platformer games that supports walking animations.
    Make sure to call update_animation after loading the animations so the
    initial texture can be set. Or manually set it.
    For a better example, see:
    http://arcade.academy/examples/platformer.html#animate-character
    """

    def __init__(self, scale: float = 1,
                 image_x: float = 0, image_y: float = 0,
                 center_x: float = 0, center_y: float = 0,
                 animations_per_second: float = 15):
        super().__init__(scale=scale, image_x=image_x, image_y=image_y,
                         center_x=center_x, center_y=center_y)
        self.state = FACE_RIGHT
        self.stand_right_textures: List[Texture] = []
        self.stand_left_textures: List[Texture] = []
        self.walk_left_textures: List[Texture] = []
        self.walk_right_textures: List[Texture] = []
        self.jumping_left_textures: List[Texture] = []
        self.jumping_right_textures: List[Texture] = []
        self.cur_texture_index = 0
        self.texture_change_distance = 20
        self.last_texture_change_center_x = 0
        self.last_texture_change_center_y = 0
        self.animations_per_second = animations_per_second
        self.time_since_last_animation = 0


    def update_animation(self, delta_time: float = 1/60):
        """
        Logic for selecting the proper texture to use.
        """
        self.time_since_last_animation += delta_time

        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        texture_list: List[Texture] = []

        change_direction = False
        if self.change_x > 0 and self.state != FACE_RIGHT:
            self.state = FACE_RIGHT
            change_direction = True

        elif self.change_x < 0 and self.state != FACE_LEFT:
            self.state = FACE_LEFT
            change_direction = True

        # If not change direction, update only each self.animations_per_second
        if self.texture is not None and not change_direction and self.time_since_last_animation <= 1.0 / self.animations_per_second:
            return
        
        if self.time_since_last_animation > 1.0 / self.animations_per_second:
            self.time_since_last_animation = 0

        if self.change_x == 0 and self.change_y == 0:
            if self.state == FACE_LEFT:
                texture_list = self.stand_left_textures

            elif self.state == FACE_RIGHT:
                texture_list = self.stand_right_textures

        elif distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == FACE_LEFT:
                texture_list = self.walk_left_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a "
                                       "list of walk left textures.")

            elif self.state == FACE_RIGHT:
                texture_list = self.walk_right_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                       "walk right textures.")


        if texture_list:
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]

        if self._texture is None:
            print("Error, no texture set")

        else:
            self.width = self._texture.width * self.scale
            self.height = self._texture.height * self.scale
