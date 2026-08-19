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
        shield_dimension: pr.Vector2,
        shield_angular_speed: float,
        shield_position_offset: int,
    ) -> None:
        self.position = position
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.guard_inner_radius = guard_inner_radius
        self.guard_outer_radius = guard_outer_radius
        self.inner_color = inner_color
        self.outer_color = outer_color
        self.shield_dimension = shield_dimension
        self.shield_angular_speed = shield_angular_speed
        self.shield_position_offset = shield_position_offset
        self.shield = Shield(
            position=pr.Vector2(
                self.position.x,
                self.position.y - self.outer_radius - self.shield_position_offset,
            ),
            width=self.shield_dimension.x,
            height=self.shield_dimension.y,
            color=pr.PURPLE,
            entity_position=self.position,
            radius=self.outer_radius + self.shield_position_offset,
            angular_speed=self.shield_angular_speed,
        )

    def get_shield(self) -> Shield:
        return self.shield

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

    def update_position(self, scale_factor, projectile_radius: int) -> None:
        self.inner_radius += scale_factor * projectile_radius
        self.outer_radius += scale_factor * projectile_radius
        self.shield.update_radius(outer_radius=self.outer_radius + self.position_offset)
