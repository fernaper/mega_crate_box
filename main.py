import arcade
import logging
import random

from entities.player import Player
from behaviours.transform import Bounce


logging.addLevelName(15, 'DEBUG_VIEW')
logging.basicConfig(level='DEBUG_VIEW')

random.seed(1)


class MegaCrateBox(arcade.Window):

    def __init__(self, width, height, title, update_rate=1/60):
        super().__init__(width, height, title)
        #self.set_location(400, 200)
        self.set_update_rate(update_rate)

        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

        self.scene_objects = [
            Player(self, 100, 100, behaviours=[
                Bounce(speed=200, direction=[1,-1], screen_collide=50)
            ]),
            Player(self, 300, 300, behaviours=[
                Bounce(speed=200, screen_collide=50)
            ]),
            Player(self, 1000, 100, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ]),
            Player(self, 100, 500, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ]),
            Player(self, 500, 500),
            Player(self, 700, 500, behaviours=[
                Bounce(speed=250, direction=[1,-1], screen_collide=50)
            ]),
        ]

        self.spatial_indexing = {}

        # Debug lines to check collisions
        self.debug_lines = []


    def on_draw(self):
        arcade.start_render()

        for scene_object in self.scene_objects:
            scene_object.on_draw()

        for debug_line in self.debug_lines:
            arcade.draw_line(*debug_line, arcade.color.WHITE)


    def on_update(self, delta_time: float):
        # Reset spatial index
        self.spatial_indexing = {}

        for scene_object in self.scene_objects:
            scene_object.on_update(delta_time)

        self.launch_collisions()


    def launch_collisions(self):
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

        for scene_object in self.scene_objects:
            minx, miny, maxx, maxy = scene_object.get_coordinates_to_check()

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
                                scene_object != c and \
                                not (scene_object in confirmated_collisions.get(c, set())) and \
                                not (scene_object in discarded_collisions.get(c, set())),
                            self.spatial_indexing[x][y]
                        )
                    )

                    for candidate in candidates:
                        if scene_object.collider.is_inside(candidate.collider):
                            if not (scene_object in confirmated_collisions):
                                confirmated_collisions[scene_object] = set()
                            confirmated_collisions[scene_object].add(candidate)

                        else:
                            if not (scene_object in discarded_collisions):
                                discarded_collisions[scene_object] = set()
                            discarded_collisions[scene_object].add(candidate)

                        if logging.root.level <= 15:
                            self.debug_lines.append((scene_object.x, scene_object.y, candidate.x, candidate.y))

        if confirmated_collisions:
            logging.info(f'Confirmated collisions: {confirmated_collisions}')

        for scene_object, collisions in confirmated_collisions.items():
            for collision_object in collisions:
                scene_object.on_collide(collision_object)
                collision_object.on_collide(scene_object)


if __name__ == '__main__':
    MegaCrateBox(1280, 720, 'MegaCrateBox')
    arcade.run()
