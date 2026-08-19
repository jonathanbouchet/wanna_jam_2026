import math
import pyray as pr
import raylib as rl
from src.utils import rotate_point


class Shield:
    def __init__(
        self,
        position,
        width: int,
        height,
        color: pr.Color,
        entity_position,
        radius: int,
        angular_speed: float,
    ) -> None:
        self.position = position  # position of the outer radius
        self.width = width
        self.height = height
        self.color = color
        self.direction = pr.Vector2(1, 0)
        self.entity_position = entity_position
        self.radius = radius
        self.angular_speed = angular_speed
        self.angle = 0.0

    def update(self, dt: float) -> None:
        self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(
            pr.is_key_down(rl.KEY_LEFT)
        )

        # origin
        origin = pr.Vector2(self.entity_position.x, self.entity_position.y)

        # update orbit angle (only changes with input)
        self.angle += self.direction.x * self.angular_speed * dt

        # constrain rectangle position to circle (constant radius)
        self.position = pr.Vector2(
            origin.x + self.radius * math.cos(self.angle),
            origin.y + self.radius * math.sin(self.angle),
        )

        self.rotation = self.angle + math.pi / 2

    def draw(self) -> None:
        # add offset to the outer radius
        # pos = pr.Vector2(self.position.x - self.width//2, self.position.y - self.height//2)
        # pr.draw_rectangle_v(pos, pr.Vector2(self.width, self.height), self.color)
        rect = pr.Rectangle(self.position.x, self.position.y, self.width, self.height)
        pr.draw_rectangle_pro(
            rect,
            pr.Vector2(self.width // 2, self.height // 2),
            self.rotation * 180 / math.pi,
            # math.degrees(math.atan2(self.direction.y, self.direction.x)),
            self.color,
        )
        coords = self.get_rectangle()
        pr.draw_line(
            int(coords[0].x),
            int(coords[0].y),
            int(coords[1].x),
            int(coords[1].y),
            pr.RED,
        )
        pr.draw_line(
            int(coords[1].x),
            int(coords[1].y),
            int(coords[2].x),
            int(coords[2].y),
            pr.RED,
        )
        pr.draw_line(
            int(coords[2].x),
            int(coords[2].y),
            int(coords[3].x),
            int(coords[3].y),
            pr.RED,
        )
        pr.draw_line(
            int(coords[3].x),
            int(coords[3].y),
            int(coords[0].x),
            int(coords[0].y),
            pr.RED,
        )

    def get_rectangle(self) -> list[pr.Vector2]:
        center = pr.Vector2(self.position.x, self.position.y)
        half = pr.Vector2(self.width / 2, self.height / 2)
        tl = pr.Vector2(center.x - half.x, center.y - half.y)
        tr = pr.Vector2(center.x + half.x, center.y - half.y)
        br = pr.Vector2(center.x + half.x, center.y + half.y)
        bl = pr.Vector2(center.x - half.x, center.y + half.y)

        angle = (
            self.rotation * 180 / math.pi
        )  # math.degrees(math.atan2(self.direction.y, self.direction.x))

        tl = rotate_point(tl, center, angle)
        tr = rotate_point(tr, center, angle)
        br = rotate_point(br, center, angle)
        bl = rotate_point(bl, center, angle)

        return [tl, tr, br, bl]

    def update_radius(self, outer_radius: int) -> None:
        self.radius = outer_radius
