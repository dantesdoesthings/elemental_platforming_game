""" Miscellaneous utils that don't fit one of the other util modules. """

from pymunk.vec2d import Vec2d


def check_grounding(player):
    """ See if the player is on the ground. Used to see if we can jump. """
    grounding = {
        'normal': Vec2d.zero(),
        'penetration': Vec2d.zero(),
        'impulse': Vec2d.zero(),
        'position': Vec2d.zero(),
        'body': None
    }

    def f(arbiter):
        normal = -arbiter.contact_point_set.normal
        if normal.y > grounding['normal'].y:
            grounding['normal'] = normal
            grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
            grounding['body'] = arbiter.shapes[1].body
            grounding['impulse'] = arbiter.total_impulse
            grounding['position'] = arbiter.contact_point_set.points[0].point_b

    player.body.each_arbiter(f)

    return grounding


def cmp(x, y):
    """Compares 2 variables, yielding -1, 0, or 1 depending on which is larger or if they're equal. """
    return (x > y) - (x < y)
