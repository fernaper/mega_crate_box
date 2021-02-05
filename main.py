import arcade
import logging
import random

from typing import Union

from entities.ball import Ball
from entities.player import Player
from entities.scene_object import SceneEntity
from behaviours.transform import Bounce


logging.addLevelName(15, 'DEBUG_VIEW')
logging.basicConfig(level='DEBUG_VIEW')

random.seed(1)


class MegaCrateBox(arcade.Window):

    CONTROLS = {
        'up': arcade.key.UP,
        'down': arcade.key.DOWN,
        'left': arcade.key.LEFT,
        'right': arcade.key.RIGHT
    }

    def __init__(self, width: int, height: int, title: str,
                 update_rate: float=1/60) -> None:
        super().__init__(width, height, title)
        #self.set_location(400, 200)
        self.set_update_rate(update_rate)
        self.scene_entities = []
        self.spatial_indexing = {}

        # Debug lines to check collisions
        self.debug_lines = []
        # All entities that observe
        self.key_observers = []

        self.setup()


    def get_control(self, key_event: str) -> Union[int, None]:
        return MegaCrateBox.CONTROLS.get(key_event)


    def setup(self) -> None:
        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

        # Add initial scene entities
        self.add_scene_entity(
            Ball(self, 100, 100, behaviours=[
                Bounce(speed=200, direction=[1,-1], screen_collide=50)
            ])
        )
        self.add_scene_entity(
            Ball(self, 300, 300, behaviours=[
                Bounce(speed=200, screen_collide=50)
            ])
        )
        self.add_scene_entity(
            Ball(self, 1000, 100, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ])
        )
        self.add_scene_entity(
            Ball(self, 100, 500, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ])
        )
        self.add_scene_entity(Ball(self, 500, 500))
        self.add_scene_entity(
            Ball(self, 700, 500, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ])
        )
        self.add_scene_entity(
            Ball(self, 800, 500, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ])
        )
        self.add_scene_entity(
            Ball(self, 500, 200, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ])
        )
        self.add_scene_entity(Ball(self, 750, 250))
        self.add_scene_entity(Player(self, 500, 100, key_observer=True))


    def add_scene_entity(self, scene_entity: SceneEntity) -> None:
        self.scene_entities.append(scene_entity)


    def add_key_observer(self, observer: SceneEntity) -> None:
        self.key_observers.append(observer)


    def on_draw(self) -> None:
        arcade.start_render()

        for scene_entity in self.scene_entities:
            scene_entity.on_draw()

        for debug_line in self.debug_lines:
            arcade.draw_line(*debug_line, arcade.color.WHITE)


    def on_update(self, delta_time: float) -> None:
        # Reset spatial index
        self.spatial_indexing = {}

        for scene_entity in self.scene_entities:
            scene_entity.on_update(delta_time)

        self.launch_collisions()


    def launch_collisions(self) -> None:
        # From one object to a set of objects
        # this way we avoid to launch two times
        # the same collision on the same object
        confirmated_collisions = {}

        # From one object to a set of objets
        # this way we avoid to check two times
        # the same negative candidates on the
        # same object
        discarded_collisions = {}

        self.debug_lines = []

        for scene_entity in self.scene_entities:
            minx, miny, maxx, maxy = scene_entity.get_coordinates_to_check()

            if None in (minx, miny, maxx, maxy):
                continue

            allx = self.spatial_indexing.keys()
            xs_to_check = list(filter(lambda x: x >= minx and x <= maxx, allx))

            for x in xs_to_check:
                ally = self.spatial_indexing[x].keys()
                ys_to_check = list(filter(lambda y: y >= miny and y <= maxy, ally))

                for y in ys_to_check:
                    candidates = list(
                        filter(
                            lambda c: \
                                scene_entity != c and \
                                not (scene_entity in confirmated_collisions.get(c, set())) and \
                                not (scene_entity in discarded_collisions.get(c, set())),
                            self.spatial_indexing[x][y]
                        )
                    )

                    for candidate in candidates:
                        if scene_entity.collider.is_inside(candidate.collider):
                            if not (scene_entity in confirmated_collisions):
                                confirmated_collisions[scene_entity] = set()
                            confirmated_collisions[scene_entity].add(candidate)

                        else:
                            if not (scene_entity in discarded_collisions):
                                discarded_collisions[scene_entity] = set()
                            discarded_collisions[scene_entity].add(candidate)

                        if logging.root.level <= 15:
                            self.debug_lines.append((scene_entity.x, scene_entity.y, candidate.x, candidate.y))

        if confirmated_collisions:
            logging.debug(f'Confirmated collisions: {confirmated_collisions}')

        for scene_entity, collisions in confirmated_collisions.items():
            for collision_object in collisions:
                scene_entity.on_collide(collision_object)
                collision_object.on_collide(scene_entity)


    def on_key_press(self, key: int, modifiers: int) -> None:
        for observer in self.key_observers:
            observer.on_key_press(key, modifiers)


    def on_key_release(self, key: int, modifiers: int) -> None:
        for observer in self.key_observers:
            observer.on_key_release(key, modifiers)


if __name__ == '__main__':
    MegaCrateBox(1280, 720, 'MegaCrateBox')
    arcade.run()
