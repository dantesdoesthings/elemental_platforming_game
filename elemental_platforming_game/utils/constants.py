import pymunk
import arcade

from elemental_platforming_game.utils import path_utils


# Window values
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
SCREEN_TITLE = 'Elemental Platformer'

# Default values
DEFAULT_MASS = 1
DEFAULT_MOMENT = pymunk.inf
DEFAULT_FRICTION = 0.5
DEFAULT_COLLISION_TYPE = 0

# Gravity
GRAVITY = (0.0, -4000.0)

# Player data
PLAYER_IMAGE_PATH = path_utils.get_resource_file_path('images/character.png')
PLAYER_MOVE_FORCE = 2000
PLAYER_JUMP_IMPULSE = 1200
PLAYER_PUNCH_IMPULSE = 600
PLAYER_MAX_HORIZONTAL_VELOCITY = 300
PLAYER_FRICTION = 0.4
PLAYER_MASS = 1
PLAYER_MOMENT = pymunk.inf
PLAYER_BODY_TYPE = pymunk.Body.DYNAMIC
PLAYER_COLLISION_TYPE = 1
PLAYER_FALL_VELOCITY = 600

# Terrain data
GRASS_IMAGE_PATH = path_utils.get_resource_file_path('images/grass_block_64_64.png')
TERRAIN_FRICTION = DEFAULT_FRICTION
TERRAIN_BODY_TYPE = pymunk.Body.STATIC
TERRAIN_COLLISION_TYPE = 2

# Keys
KEY_UP = frozenset({arcade.key.UP, arcade.key.W})
KEY_DOWN = frozenset({arcade.key.DOWN, arcade.key.S})
KEY_LEFT = frozenset({arcade.key.LEFT, arcade.key.A})
KEY_RIGHT = frozenset({arcade.key.RIGHT, arcade.key.D})

# Grid-size
SPRITE_SIZE = 64

# How close we get to the edge before scrolling
VIEWPORT_MARGIN = 150