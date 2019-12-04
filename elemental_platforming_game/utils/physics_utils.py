import math


def resync_physics_sprites(sprite_list):
    """ Move sprites to where physics objects are """
    for sprite in sprite_list:
        sprite.center_x = sprite.shape.body.position.x
        sprite.center_y = sprite.shape.body.position.y
        sprite.angle = math.degrees(sprite.shape.body.angle)
