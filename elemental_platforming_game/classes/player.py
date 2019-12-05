"""Defines the Player class."""

import pymunk

from elemental_platforming_game.utils.constants import *
from elemental_platforming_game.classes import physics_sprite


class Player(physics_sprite.PhysicsSprite):

    def __init__(self,
                 scale=PLAYER_SCALE,
                 center_x=0,
                 center_y=0):
        """The player matches up to a pymunk Body as well as being an arcade Sprite."""

        shape = pymunk.Circle(None, 32)

        super().__init__(PLAYER_IMAGE_PATH, center_x=center_x, center_y=center_y, scale=scale,
                         mass=PLAYER_MASS, moment=PLAYER_MOMENT, body_type=PLAYER_BODY_TYPE,
                         friction=PLAYER_MOVING_FRICTION, collision_type=PLAYER_COLLISION_TYPE, shape=shape)

        def limit_velocity(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, gravity, damping, dt)
            horiz_vel = body.velocity.x
            if horiz_vel > PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)
            elif horiz_vel < -PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(-PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)

        self.body.velocity_func = limit_velocity

        self.body2 = pymunk.Body(PLAYER_MASS, PLAYER_SPRITE_MOMENT, body_type=PLAYER_BODY_TYPE)
        self.body2.position = self.body.position
        self.shape2 = pymunk.Circle(self.body2, 32)
        self.shape2.friction = 0.5
        self.shape2.collision_type = PLAYER_COLLISION_TYPE

        def limit_velocity2(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, (0, 0), damping, dt)
            horiz_vel = body.velocity.x
            if horiz_vel > PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)
            elif horiz_vel < -PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(-PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)

        self.body2.velocity_func = limit_velocity2

        self.shape.filter = pymunk.ShapeFilter(group=1, categories=0b1)
        self.shape2.filter = pymunk.ShapeFilter(group=1, categories=0b1)
