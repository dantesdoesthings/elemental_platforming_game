"""Defines the Player class."""

import pymunk
import arcade

from elemental_platforming_game.utils.constants import *
from elemental_platforming_game.classes import physics_sprite


class Player(physics_sprite.PhysicsSprite):

    def __init__(self,
                 scale=PLAYER_SCALE,
                 center_x=0,
                 center_y=0):
        """The player matches up to a pymunk Body as well as being an arcade Sprite."""

        shape = pymunk.Circle(None, 32)

        super().__init__(PLAYER_WHEEL_IMAGE_PATH, center_x=center_x, center_y=center_y, scale=scale,
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

        # Torso
        self.torso_shape = pymunk.Poly(self.body, [(0, 0), (0, 63), (95, 63), (95, 0)])
        self.torso_shape.friction = self.shape.friction
        self.torso_shape.collision_type = self.shape.collision_type
        self.torso_sprite = arcade.Sprite(PLAYER_TORSO_IMAGE_PATH, scale=scale, center_x=center_x, center_y=center_y)
        self.torso_sprite.resync = lambda: None

        # Spinning wheel
        self.spinning_body = pymunk.Body(PLAYER_MASS, PLAYER_SPRITE_MOMENT, body_type=PLAYER_BODY_TYPE)
        self.spinning_body.position = self.body.position
        self.spinning_shape = pymunk.Circle(self.spinning_body, 32)
        self.spinning_shape.friction = 0.5
        self.spinning_shape.collision_type = PLAYER_COLLISION_TYPE

        def limit_velocity2(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, (0, 0), damping, dt)
            horiz_vel = body.velocity.x
            if horiz_vel > PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)
            elif horiz_vel < -PLAYER_MAX_HORIZONTAL_VELOCITY:
                body.velocity = pymunk.Vec2d(-PLAYER_MAX_HORIZONTAL_VELOCITY, body.velocity.y)

        self.spinning_body.velocity_func = limit_velocity2

        self.shape.filter = pymunk.ShapeFilter(group=1, categories=0b1)
        self.spinning_shape.filter = pymunk.ShapeFilter(group=1, categories=0b1)

    def resync(self):
        """ Resyncs the sprite to the pymunk Body """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.angle = math.degrees(self.spinning_shape.body.angle)
        self.torso_sprite.center_x = self.shape.body.position.x
        self.torso_sprite.center_y = self.shape.body.position.y + 32  # TODO: TEMP SOLUTION
