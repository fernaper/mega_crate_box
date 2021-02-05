from __future__ import annotations

import arcade
import logging
import math

from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.scene_object import SceneEntity


class Collider():

    def __init__(self, parent: 'SceneEntity'=None) -> None:
        self.parent = parent


    def set_parent(self, parent: 'SceneEntity') -> None:
        self.parent = parent


    def is_inside(self, other_collider: Collider) -> bool:
        return False


    def get_coordinates_to_check(self) -> Tuple[float,float,float,float]:
        return (
            self.parent.x - 10,
            self.parent.y - 10,
            self.parent.x + 10,
            self.parent.y + 10
        )


class CircleCollider(Collider):


    MARGIN_TO_CHECK = 100


    def __init__(self, parent: 'SceneEntity', radius: float, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.radius = radius


    def is_inside(self, other_collider: Collider) -> bool:
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


    def get_coordinates_to_check(self) -> Tuple[float,float,float,float]:
        return (
            self.parent.x - self.radius - CircleCollider.MARGIN_TO_CHECK,
            self.parent.y - self.radius - CircleCollider.MARGIN_TO_CHECK,
            self.parent.x + self.radius + CircleCollider.MARGIN_TO_CHECK,
            self.parent.y + self.radius + CircleCollider.MARGIN_TO_CHECK,
        )


class BoxCollider(Collider):

    def __init__(self, parent: Collider, width: float, height: float, **kwargs) -> None:
        super().__init__(parent, **kwargs)


class PloygonCollider(Collider):

    def __init__(self, parent: Collider, polygon: List[float], **kwargs) -> None:
        super().__init__(parent, **kwargs)

