import pyray as pr
from src.shield import Shield


class Entity:
    def __init__(
        self,
        position: pr.Vector2,
        inner_radius: int,
        outer_radius: int,
        guard_inner_radius: int,
        guard_outer_radius: int,
        inner_color: pr.Color,
        outer_color: pr.Color,
    ) -> None:
        self.position = position
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.guard_inner_radius = guard_inner_radius
        self.guard_outer_radius = guard_outer_radius
        self.inner_color = inner_color
        self.outer_color = outer_color
        self.shield = Shield(
            position=pr.Vector2(self.position.x, self.position.y - self.outer_radius - 10), 
            width=100, 
            height=10, 
            color=pr.PURPLE, 
            entity_position=self.position,
            radius = 100
        )

    def update(self, dt: float) -> None:
        self.shield.update(dt=dt)
        self.check_guard()

    def check_guard(self) -> None:
        if self.outer_radius >= self.guard_inner_radius:
            self.inner_color = pr.RED
            self.outer_color = pr.PINK

    def draw(self) -> None:
        pr.draw_ring(
            self.position,
            self.inner_radius,
            self.outer_radius,
            0,
            360,
            50,
            self.outer_color,
        )
        pr.draw_circle_v(self.position, self.inner_radius, self.inner_color)
        self.draw_guard_radius()
        self.shield.draw()

    def draw_guard_radius(self) -> None:
        for i in range(9):
            start = i * 45
            pr.draw_ring_lines(
                self.position,
                self.guard_inner_radius,
                self.guard_outer_radius,
                start,
                start + 30,
                50,
                pr.YELLOW,
            )
