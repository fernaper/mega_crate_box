import math

from behaviours.behaviour import Behaviour


class Transform(Behaviour):

    def __init__(self):
        ...


class Bounce(Transform):

    def __init__(self, speed: float=1000, direction: 'List[float]'=[1,1], screen_collide: float=0.0):
        self.speed = speed
        self.direction = direction
        self.screen_collide = screen_collide


    def on_update(self, delta_time: float):
        self.parent.x += self.speed * self.direction[0] * delta_time
        self.parent.y += self.speed * self.direction[1] * delta_time

        width, height = self.parent.window.get_size()

        if self.parent.x + self.screen_collide >= width or self.parent.x - self.screen_collide <= 0:
            self.direction[0] = (-1 if self.parent.x + self.screen_collide >= width else 1) * abs(self.direction[0])
        if self.parent.y + self.screen_collide >= height or self.parent.y - self.screen_collide <= 0:
            self.direction[1] = (-1 if self.parent.y + self.screen_collide >= height else 1) * abs(self.direction[1])


    def on_collide(self, other):
        # First get normalized directional vector
        distance = [self.parent.x - other.x, self.parent.y - other.y]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]

        #if direction[0] < 0 and self.xspeed > 0 or direction[0] > 0 and self.xspeed < 0:
        self.direction[0] = direction[0]
        #if direction[1] < 0 and self.yspeed > 0 or direction[1] > 0 and self.yspeed < 0:
        self.direction[1] = direction[1]
