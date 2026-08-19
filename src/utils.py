import math
import pyray as pr


def rotate_point(p: pr.Vector2, center: pr.Vector2, angle_deg: float) -> pr.Vector2:
    """
    - perform a rotation of point around center
    - rotation is done in local coordinate of the rectangle
    """
    a = math.radians(angle_deg)
    s, c = math.sin(a), math.cos(a)
    # translate to center
    x, y = p.x - center.x, p.y - center.y
    # rotate
    xr = x * c - y * s
    yr = x * s + y * c
    # translate back
    return pr.Vector2(center.x + xr, center.y + yr)


def rotate_xz(x: float, y: float, z: float, da: float):
    """rotate a vertex in the xz plane (around y)"""
    c = math.cos(da)
    s = math.sin(da)
    return x * c - z * s, y, x * s + z * c
