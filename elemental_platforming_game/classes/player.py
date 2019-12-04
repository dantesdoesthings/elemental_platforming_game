"""Defines the Player class."""

import pymunk

from elemental_platforming_game.utils.constants import *
from elemental_platforming_game.classes import physics_sprite


class Player(physics_sprite.PhysicsSprite):

    def __init__(self,
                 scale=0.5,
                 center_x=0,
                 center_y=0):
        """The player matches up to a pymunk Body as well as being an arcade Sprite."""
        super().__init__(PLAYER_IMAGE_PATH, center_x=center_x, center_y=center_y, scale=scale,
                         mass=PLAYER_MASS, moment=PLAYER_MOMENT, body_type=PLAYER_BODY_TYPE,
                         friction=PLAYER_FRICTION, collision_type=PLAYER_COLLISION_TYPE)

        def limit_velocity(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, gravity, damping, dt)
            horiz_vel = body.velocity.x
            if horiz_vel > PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)
            elif horiz_vel < -PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(-PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)

        self.body.velocity_func = limit_velocity
