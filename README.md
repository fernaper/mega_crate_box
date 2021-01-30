# Mega Crate Box

Based on the original game, [Super Crate Box](http://supercratebox.com/) I decided to create **Mega Crate Box**.
The idea is to get the maximum number of crates while climbing the scenario while enemies try to kill us.

# How is it done?

It is done in Python with the library [arcade](https://arcade.academy/).
I create my own engine based on Unity concepts.

Right now the system has **Entities**, each entity has **Behaviours** and can have **Colliders**.
This structures makes the `on_draw` and `on_update` methods really easy to manage.
In fact there is no need to change that loop. You can just add items to the scene.

