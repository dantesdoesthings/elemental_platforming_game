"""
Main window and functionality module.
"""

import arcade
import pymunk

from elemental_platforming_game.utils import path_utils
from elemental_platforming_game.examples.create_level import create_level_1
from elemental_platforming_game.examples.physics_utility import (
    PymunkSprite,
    check_grounding,
    resync_physics_sprites,
)

from elemental_platforming_game.utils.constants import *


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.space.collision_bias = 0

        # Physics joint used for grabbing items
        self.grab_joint = None

        # Lists of sprites
        self.dynamic_sprite_list = arcade.SpriteList[PymunkSprite]()
        self.static_sprite_list = arcade.SpriteList()

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        # Current force applied to the player for movement by keyboard
        self.force = [0, 0]

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        create_level_1(self.space, self.static_sprite_list, self.dynamic_sprite_list)

        # Create player
        x = 50
        y = (SPRITE_SIZE + SPRITE_SIZE / 2)
        self.player = PymunkSprite(path_utils.get_resource_file_path("images/character.png"),
                                   x, y, scale=0.5, moment=pymunk.inf, mass=1, friction=PLAYER_FRICTION)
        self.dynamic_sprite_list.append(self.player)
        self.space.add(self.player.body, self.player.shape)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites
        self.static_sprite_list.draw()
        self.dynamic_sprite_list.draw()

        # Display speeds
        txt1 = f'ΔX : {self.player.body.velocity.x}'
        txt2 = f'ΔY : {self.player.body.velocity.y}'
        arcade.draw_text(txt1, 20 + self.view_left, SCREEN_HEIGHT - 20 + self.view_bottom, arcade.color.WHITE, 12)
        arcade.draw_text(txt2, 20 + self.view_left, SCREEN_HEIGHT - 40 + self.view_bottom, arcade.color.WHITE, 12)

        # Display instructions
        output = "Use the mouse to move boxes, space to punch, hold G to grab an item to the right."
        arcade.draw_text(output, 20 + self.view_left, SCREEN_HEIGHT - 60 + self.view_bottom, arcade.color.WHITE, 12)

    # def on_mouse_press(self, x, y, button, modifiers):
    #     """ Handle mouse down events """
    #
    #     if button == arcade.MOUSE_BUTTON_LEFT:
    #
    #         # Store where the mouse is clicked. Adjust accordingly if we've
    #         # scrolled the viewport.
    #         self.last_mouse_position = (x + self.view_left, y + self.view_bottom)
    #
    #         # See if we clicked on any physics object
    #         shape_list = self.space.point_query(self.last_mouse_position, 1, pymunk.ShapeFilter())
    #
    #         # If we did, remember what we clicked on
    #         if len(shape_list) > 0:
    #             self.shape_being_dragged = shape_list[0]

    # def on_mouse_release(self, x, y, button, modifiers):
    #     """ Handle mouse up events """
    #
    #     if button == arcade.MOUSE_BUTTON_LEFT:
    #         # Release the item we are holding (if any)
    #         self.shape_being_dragged = None

    # def on_mouse_motion(self, x, y, dx, dy):
    #     """ Handle mouse motion events """
    #
    #     if self.shape_being_dragged is not None:
    #         # If we are holding an object, move it with the mouse
    #         self.last_mouse_position = (x + self.view_left, y + self.view_bottom)
    #         self.shape_being_dragged.shape.body.position = self.last_mouse_position
    #         self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    def scroll_viewport(self):
        """ Manage scrolling of the viewport. """

        # Flipped to true if we need to scroll
        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_bndry:
            self.view_left -= left_bndry - self.player.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_bndry:
            self.view_bottom += self.player.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_update(self, delta_time):
        """ Update the sprites """

        # If we have force to apply to the player (from hitting the arrow
        # keys), apply it.
        self.player.body.apply_force_at_local_point(self.force, (0, 0))

        # check_collision(self.player)

        # See if the player is standing on an item.
        # If she is, apply opposite force to the item below her.
        # So if she moves left, the box below her will have
        # a force to move to the right.
        # grounding = check_grounding(self.player)
        # if self.force[0] and grounding and grounding['body']:
        #     grounding['body'].apply_force_at_world_point((-self.force[0], 0), grounding['position'])

        # Check for sprites that fall off the screen.
        # If so, get rid of them.
        # for sprite in self.dynamic_sprite_list:
        #     if sprite.shape.body.position.y < 0:
        #         # Remove sprites from physics space
        #         self.space.remove(sprite.shape, sprite.shape.body)
        #         # Remove sprites from physics list
        #         sprite.remove_from_sprite_lists()

        # Update physics
        # Use a constant time step, don't use delta_time
        # See "Game loop / moving time forward"
        # http://www.pymunk.org/en/latest/overview.html#game-loop-moving-time-forward
        self.space.step(1 / 60.0)

        # If we are dragging an object, make sure it stays with the mouse. Otherwise
        # gravity will drag it down.
        # if self.shape_being_dragged is not None:
        #     self.shape_being_dragged.shape.body.position = self.last_mouse_position
        #     self.shape_being_dragged.shape.body.velocity = 0, 0

        # Resync the sprites to the physics objects that shadow them
        resync_physics_sprites(self.dynamic_sprite_list)

        # Scroll the viewport if needed
        self.scroll_viewport()

    def punch(self):
        # --- Punch left
        # See if we have a physics object to our right
        check_point = (self.player.right + 10, self.player.center_y)
        shape_list = self.space.point_query(check_point, 1, pymunk.ShapeFilter())

        # Apply force to any object to our right
        for shape in shape_list:
            shape.shape.body.apply_impulse_at_world_point((PLAYER_PUNCH_IMPULSE, PLAYER_PUNCH_IMPULSE),
                                                          check_point)

        # --- Punch right
        # See if we have a physics object to our left
        check_point = (self.player.left - 10, self.player.center_y)
        shape_list = self.space.point_query(check_point, 1, pymunk.ShapeFilter())

        # Apply force to any object to our right
        for shape in shape_list:
            shape.shape.body.apply_impulse_at_world_point((-PLAYER_PUNCH_IMPULSE, PLAYER_PUNCH_IMPULSE),
                                                          check_point)

    def grab(self):
        """ Grab something """
        # See if we have a physics object to our right
        check_point = (self.player.right + 10, self.player.center_y)
        shape_list = self.space.point_query(check_point, 1, pymunk.ShapeFilter())

        # Create a joint for an item to our right
        for shape in shape_list:
            self.grab_joint = pymunk.PinJoint(self.player.shape.body, shape.shape.body)
            self.space.add(self.grab_joint)

    def let_go(self):
        """ Let go of whatever we are holding """
        if self.grab_joint:
            self.space.remove(self.grab_joint)
            self.grab_joint = None

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard presses. """
        if symbol == arcade.key.RIGHT:
            # Add force to the player, and set the player friction to zero
            self.force[0] += PLAYER_MOVE_FORCE
        elif symbol == arcade.key.LEFT:
            # Add force to the player, and set the player friction to zero
            self.force[0] -= PLAYER_MOVE_FORCE
        elif symbol == arcade.key.UP:
            # find out if player is standing on ground
            grounding = check_grounding(self.player)
            if grounding['body'] is not None and abs(
                    grounding['normal'].x / grounding['normal'].y) < self.player.shape.friction:
                # She is! Go ahead and jump
                self.player.body.apply_impulse_at_local_point((0, PLAYER_JUMP_IMPULSE))
        elif symbol == arcade.key.SPACE:
            self.punch()
        elif symbol == arcade.key.G:
            self.grab()

    def on_key_release(self, symbol: int, modifiers: int):
        """ Handle keyboard releases. """
        if symbol == arcade.key.RIGHT:
            # Remove force from the player, and set the player friction to a high number so she stops
            self.force[0] -= PLAYER_MOVE_FORCE
        elif symbol == arcade.key.LEFT:
            # Remove force from the player, and set the player friction to a high number so she stops
            self.force[0] += PLAYER_MOVE_FORCE
        elif symbol == arcade.key.G:
            self.let_go()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()


if __name__ == "__main__":
    main()