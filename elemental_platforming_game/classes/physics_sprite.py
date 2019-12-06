"""Defines the Player class."""

import arcade
import pymunk
import math

from elemental_platforming_game.utils.constants import \
    DEFAULT_MASS, DEFAULT_MOMENT, DEFAULT_FRICTION, DEFAULT_COLLISION_TYPE


class PhysicsSprite(arcade.Sprite):

    def __init__(self,
                 filename: str,
                 center_x: int = 0,
                 center_y: int = 0,
                 scale: float = 1.,
                 mass: float = DEFAULT_MASS,
                 moment: float = DEFAULT_MOMENT,
                 body_type=pymunk.Body.DYNAMIC,
                 friction: float = DEFAULT_FRICTION,
                 collision_type: int = DEFAULT_COLLISION_TYPE,
                 shape: pymunk.Shape = None):
        """The PhysicsSprite matches up to a pymunk Body as well as being an arcade Sprite."""
        super().__init__(filename, scale=scale, center_x=center_x, center_y=center_y)

        self.width = self.texture.width * scale
        self.height = self.texture.height * scale

        self.body = pymunk.Body(mass, moment, body_type=body_type)
        self.body.position = pymunk.Vec2d(center_x, center_y)
        if shape is not None:
            self.shape = shape
            self.shape.body = self.body
        else:
            self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.friction = friction
        self.shape.collision_type = collision_type

    def resync(self):
        """ Resyncs the sprite to the pymunk Body """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.angle = math.degrees(self.shape.body.angle)
