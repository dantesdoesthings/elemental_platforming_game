"""Defines the Player class."""

import arcade
import pymunk

from elemental_platforming_game.utils.constants import \
    TERRAIN_FRICTION, TERRAIN_BODY_TYPE, TERRAIN_COLLISION_TYPE
from elemental_platforming_game.classes import physics_sprite


class Terrain(physics_sprite.PhysicsSprite):

    def __init__(self,  # TODO: Size of terrain hookup
                 filename,
                 scale=0.5,
                 center_x=0,
                 center_y=0):
        """The player matches up to a pymunk Body as well as being an arcade Sprite."""
        super().__init__(filename, center_x=center_x, center_y=center_y, scale=scale,
                         body_type=TERRAIN_BODY_TYPE,
                         friction=TERRAIN_FRICTION, collision_type=TERRAIN_COLLISION_TYPE)
