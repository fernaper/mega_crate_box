class Behaviour():

    def __init__(self, *args, **kwargs):
        self.parent = None


    def set_parent(self, parent):
        self.parent = parent


    def on_update(self, delta_time):
        ...


    def on_collide(self, other):
        ...
