"""
Main window and functionality module.
"""

import arcade
import pymunk

from elemental_platforming_game.utils.constants import *
from elemental_platforming_game.classes.player import Player
from elemental_platforming_game.utils import physics_utils, misc

USE_FORCE = True


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(BACKGROUND_COLOR)

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # -- Pymunk
        self.space = None
        self.force = 0, 0

        # Game objects
        self.player = None

        # Lists of sprites
        self.dynamic_sprite_list = None
        self.static_sprite_list = None

        # Movement state
        self.push_direction = 0

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Game objects
        self.player = Player(center_x=100, center_y=100)

        # Lists of sprites
        self.dynamic_sprite_list = arcade.SpriteList()
        self.static_sprite_list = arcade.SpriteList()
        self.dynamic_sprite_list.append(self.player)

        # Pymunk
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.force = [0, 0]

        self.space.add(self.player.body, self.player.shape, self.player.spinning_body, self.player.spinning_shape)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites
        self.static_sprite_list.draw()
        self.dynamic_sprite_list.draw()

        # TODO: TEMPORARY
        arcade.draw_rectangle_filled(450, 25, 900, 50, arcade.color.GRAY_BLUE, 0)
        floor = pymunk.Poly(self.space.static_body, [(0, 0), (900, 0), (900, 50), (0, 50)])
        hill = pymunk.Poly(self.space.static_body, [[350, 25], [575,300], [675,300], [900, 25]])
        floor.friction = DEFAULT_FRICTION
        hill.friction = DEFAULT_FRICTION
        self.space.add(floor)
        self.space.add(hill)
        # Display speeds
        txt1 = f'ΔX : {self.player.body.velocity.x}'
        txt2 = f'ΔY : {self.player.body.velocity.y}'
        arcade.draw_text(txt1, 20 + self.view_left, SCREEN_HEIGHT - 20 + self.view_bottom, TEXT_COLOR, 12)
        arcade.draw_text(txt2, 20 + self.view_left, SCREEN_HEIGHT - 40 + self.view_bottom, TEXT_COLOR, 12)
        # arcade.draw_circle_filled(self.player.spinning_body.position.x, self.player.spinning_body.position.y, 32, arcade.color.GRAY)
        arcade.draw_polygon_filled([[350, 25], [575,300], [675,300], [900, 25]], arcade.color.GRAY_ASPARAGUS)

    def scroll_viewport(self):
        """ Manage scrolling of the viewport. """

        # Flipped to true if we need to scroll
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_update(self, delta_time):
        """ Update the sprites """

        # Find out and handle the player standing on the ground
        grounding = misc.check_grounding(self.player)

        # If we have force to apply to the player (from hitting the arrow
        # keys), apply it.
        if USE_FORCE:
            self.player.body.apply_force_at_local_point(self.force, (0, 0))

        # Max falling velocity
        # self.player.body.velocity.y = max(self.player.body.velocity.y, -PLAYER_FALL_VELOCITY)  # TODO: This doesn't work

        # Angular velocity
        push_direction = misc.cmp(self.push_direction, 0)
        if push_direction:
            self.player.spinning_body.angular_velocity = PLAYER_ANGULAR_VELOCITY_MULTIPLIER * \
                max((abs(self.player.body.velocity.x), PLAYER_MAX_HORIZONTAL_VELOCITY / 2)) * push_direction
        else:
            move_direction = misc.cmp(self.player.body.velocity.x, 0)
            self.player.spinning_body.angular_velocity = PLAYER_ANGULAR_VELOCITY_MULTIPLIER * \
                abs(self.player.body.velocity.x) * move_direction

        # ---- Final steps to apply the update ---
        # PyMunk space update
        self.space.step(1 / 60.0)

        # Resync the sprites to the physics objects that shadow them
        [sprite.resync() for sprite in self.dynamic_sprite_list]

        # Scroll the viewport if needed
        self.scroll_viewport()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard presses. """
        if symbol in KEY_RIGHT:
            # Add force to the player, and set the player friction to zero
            self.press_right()
        elif symbol in KEY_LEFT:
            # Add force to the player, and set the player friction to zero
            self.press_left()
        elif symbol in KEY_UP:
            # find out if player is standing on ground
            grounding = misc.check_grounding(self.player)
            if grounding['body'] is not None and abs(
                    grounding['normal'].x / grounding['normal'].y) < PLAYER_MAX_ALLOWABLE_JUMP_ANGLE:
                self.player.body.apply_impulse_at_local_point((0, PLAYER_JUMP_IMPULSE))
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, symbol: int, modifiers: int):
        """ Handle keyboard releases. """
        if symbol in KEY_RIGHT:
            # Remove force from the player
            self.release_right()
        elif symbol in KEY_LEFT:
            # Remove force from the player
            self.release_left()

    def press_right(self):
        """ Handle moving right """
        self.push_direction += 1
        self.move_player()

    def press_left(self):
        """ Handle moving left """
        self.push_direction -= 1
        self.move_player()

    def release_right(self):
        """ Handle letting go of the right key """
        self.push_direction -= 1
        self.move_player()

    def release_left(self):
        """ Handle letting go of the left key """
        self.push_direction += 1
        self.move_player()

    # def stop_player(self):
    #     """ Handle removing all player impulse """
    #     self.player.force = 0, 0
    #     # self.player.shape.surface_velocity = 0, 0
    #     self.player.shape.friction = PLAYER_STOPPING_FRICTION

    def move_player(self):
        """ Handle setting player impulse """
        if USE_FORCE:
            if self.push_direction > 0:
                self.force = PLAYER_MOVE_FORCE, 0
                self.player.shape.friction = PLAYER_MOVING_FRICTION
            elif self.push_direction < 0:
                self.force = - PLAYER_MOVE_FORCE, 0
                self.player.shape.friction = PLAYER_MOVING_FRICTION
            else:
                self.force = 0, 0
                self.player.shape.friction = PLAYER_STOPPING_FRICTION
        else:
            if self.push_direction > 0:
                self.player.shape.surface_velocity = - PLAYER_MAX_HORIZONTAL_VELOCITY, 0
                self.player.shape.friction = PLAYER_MOVING_FRICTION
            elif self.push_direction < 0:
                self.player.shape.surface_velocity = PLAYER_MAX_HORIZONTAL_VELOCITY, 0
                self.player.shape.friction = PLAYER_MOVING_FRICTION
            else:
                self.player.shape.surface_velocity = 0, 0
                self.player.shape.friction = PLAYER_STOPPING_FRICTION


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
