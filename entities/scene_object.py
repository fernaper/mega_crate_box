import arcade
import itertools
import logging

from pyglet.gl import GL_NEAREST


class SceneEntity():

    counter_id = itertools.count()

    def __init__(self, window, x, y, behaviours=[], collider=None, key_observer=False, **kwargs):
        self.id = next(SceneEntity.counter_id)
        self.window = window
        self.x = x
        self.y = y
        self.collider = collider
        self.key_observer = key_observer

        if self.key_observer:
            self.window.add_key_observer(self)

        for behaviour in behaviours:
            behaviour.set_parent(self)

        self.behaviours = behaviours

        self.sprite_list = None
        self.animation = None
        self.setup()


    def setup(self):
        ...


    def on_draw(self):
        if self.sprite_list is not None:
            self.sprite_list.draw(filter=GL_NEAREST)

        if logging.root.level <= 15:
            arcade.draw_text(
                str(self.id), self.x - 5, self.y - 10, arcade.color.WHITE, font_size=20
            )


    def on_update(self, delta_time):
        if self.sprite_list:
            self.sprite_list.update()
            self.sprite_list.update_animation()

        if self.animation:
            self.x = self.animation.center_x
            self.y = self.animation.center_y

        for behaviour in self.behaviours:
            behaviour.on_update(delta_time)

        # Prepare all the colliders
        if not self.collider:
            return

        if self.x not in self.window.spatial_indexing:
            self.window.spatial_indexing[self.x] = {
                self.y: [self]
            }

        elif self.y not in self.window.spatial_indexing[self.x]:
            self.window.spatial_indexing[self.x][self.y] = [self]

        else:
            self.window.spatial_indexing[self.x][self.y].append(self)


    def get_coordinates_to_check(self):
        if self.collider is None:
            return None, None, None, None

        else:
            return self.collider.get_coordinates_to_check()


    def on_collide(self, other):
        logging.debug(f'[COLLISION] {self} <= = => {other}.')
        for behaviour in self.behaviours:
            behaviour.on_collide(other)


    def on_key_press(self, key, modifiers):
        ...


    def on_key_release(self, key, modifiers):
        ...


    def __str__(self):
        return f'<Object:{self.id}; x:{self.x}; y:{self.y}>'
