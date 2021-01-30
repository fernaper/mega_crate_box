import arcade
import logging
import math


class Collider():

    def __init__(self, parent=None):
        self.parent = parent


    def set_parent(self, parent):
        self.parent = parent


    def is_inside(self, other_collider):
        return False


    def get_coordinates_to_check(self):
        return (
            self.parent.x - 10,
            self.parent.y - 10,
            self.parent.x + 10,
            self.parent.y + 10
        )


class CircleCollider(Collider):


    MARGIN_TO_CHECK = 100


    def __init__(self, parent, radius: float, **kwargs):
        super().__init__(parent, **kwargs)
        self.radius = radius


    def is_inside(self, other_collider):
        response = False
        x, y = self.parent.x, self.parent.y
        x2, y2 = other_collider.parent.x, other_collider.parent.y

        if isinstance(other_collider, CircleCollider):
            distance = pow(x - x2, 2) + pow(y - y2, 2)
            radius_sum = pow(self.radius + other_collider.radius, 2)
            return distance <= radius_sum

        elif isinstance(other_collider, BoxCollider):
            ...

        elif isinstance(other_collider, PloygonCollider):
            ...

        return response


    def get_coordinates_to_check(self):
        return (
            self.parent.x - self.radius - CircleCollider.MARGIN_TO_CHECK,
            self.parent.y - self.radius - CircleCollider.MARGIN_TO_CHECK,
            self.parent.x + self.radius + CircleCollider.MARGIN_TO_CHECK,
            self.parent.y + self.radius + CircleCollider.MARGIN_TO_CHECK,
        )


class BoxCollider(Collider):

    def __init__(self, parent, width: float, height: float, **kwargs):
        super().__init__(parent, **kwargs)


class PloygonCollider(Collider):

    def __init__(self, parent, polygon: 'list[float]', **kwargs):
        super().__init__(parent, **kwargs)

