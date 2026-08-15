import pyray as pr

class Entity:
    def __init__(self, position: pr.Vector2, inner_radius: int, outer_radius: int, inner_color: pr.Color, outer_color: pr.Color) -> None:
        self.position = position
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.inner_color = inner_color
        self.outer_color = outer_color

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pr.draw_ring(
            self.position, 
            self.inner_radius, 
            self.outer_radius, 
            0, 
            360, 
            50, 
            self.outer_color
        )
        pr.draw_circle_v(self.position, self.inner_radius, self.inner_color)
