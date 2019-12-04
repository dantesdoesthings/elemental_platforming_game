"""Defines the Player class."""

import arcade
import pymunk

from elemental_platforming_game.utils.constants import \
    DEFAULT_MASS, DEFAULT_MOMENT, DEFAULT_FRICTION, DEFAULT_COLLISION_TYPE


class PhysicsSprite(arcade.Sprite):

    def __init__(self,
                 filename,
                 center_x=0,
                 center_y=0,
                 scale=1,
                 mass=DEFAULT_MASS,
                 moment=DEFAULT_MOMENT,
                 body_type=pymunk.Body.DYNAMIC,
                 friction=DEFAULT_FRICTION,
                 collision_type=DEFAULT_COLLISION_TYPE):
        """The PhysicsSprite matches up to a pymunk Body as well as being an arcade Sprite."""
        super().__init__(filename, scale=scale, center_x=center_x, center_y=center_y)

        self.width = self.texture.width * scale
        self.height = self.texture.height * scale

        self.body = pymunk.Body(mass, moment, body_type=body_type)
        self.body.position = pymunk.Vec2d(center_x, center_y)
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.friction = friction
        self.shape.collision_type = collision_type
