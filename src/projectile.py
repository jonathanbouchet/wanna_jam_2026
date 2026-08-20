import pyray as pr

from src.utils import rotate_point


class Projectile:
    def __init__(
        self,
        position: pr.Vector2,
        radius: int,
        speed: int,
        direction: pr.Vector2,
        color: pr.Color,
        game_window: pr.Vector2,
    ) -> None:
        self.position = position
        self.direction = direction
        self.speed = speed
        self.radius = radius
        self.color = color
        self.game_window = game_window
        self.is_disabled = False
        self.angle = 0

    def move(self, dt: float) -> None:
        """
        - check for collisions with the top, bottom, left and right border of the screen in order to make the ring bouncing back
        """

        if (
            self.position.x >= (self.game_window.x - self.radius)
            or self.position.x <= self.radius
        ):
            self.direction.x *= -1
        if (
            self.position.y >= (self.game_window.y - self.radius)
            or self.position.y <= self.radius
        ):
            self.direction.y *= -1

        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def update(self, dt):
        self.move(dt)

    def draw(self):
        pr.draw_circle_v(self.position, self.radius, self.color)
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
        # make a pr.Rectangle based on the projectile radius
        # TEST
        center = self.position

        half = pr.Vector2(self.radius, self.radius)
        tl = pr.Vector2(center.x - half.x, center.y - half.y)
        tr = pr.Vector2(center.x + half.x, center.y - half.y)
        br = pr.Vector2(center.x + half.x, center.y + half.y)
        bl = pr.Vector2(center.x - half.x, center.y + half.y)

        tl = rotate_point(tl, center, self.angle)
        tr = rotate_point(tr, center, self.angle)
        br = rotate_point(br, center, self.angle)
        bl = rotate_point(bl, center, self.angle)

        return [tl, tr, br, bl]

    def __str__(self) -> str:
        return f"speed: {self.speed}, radius: {self.radius}, color: {self.color}"
