from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.scene_object import SceneEntity


class Behaviour():

    def __init__(self, *args, **kwargs) -> None:
        self.parent = None


    def set_parent(self, parent: 'SceneEntity') -> None:
        self.parent = parent


    def on_update(self, delta_time: float) -> None:
        ...


    def on_collide(self, other: 'SceneEntity') -> None:
        ...
