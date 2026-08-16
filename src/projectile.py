import pyray as pr


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

    def __str__(self) -> str:
        return f"speed: {self.speed}, radius: {self.radius}, color: {self.color}"
