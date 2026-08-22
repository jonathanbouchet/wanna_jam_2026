import pyray as pr


class Button:
    def __init__(
        self,
        position: pr.Vector2,
        size: pr.Vector2,
        text: str,
        font: pr.Font,
        font_size: int,
        font_color: pr.Color,
        font_highlight_color: pr.Color
    ) -> None:
        self.position = position
        self.size = size
        self.rect = pr.Rectangle(
            self.position.x - 10, self.position.y, self.size.x, self.size.y - 5
        )
        self.state_changed = False
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.highlighted_color = font_highlight_color
        self.current_color = self.font_color
        self.is_clicked = False

    def draw(self) -> None:
        pr.draw_text_ex(
            self.font, self.text, self.position, self.font_size, 2, self.current_color
        )
        pr.draw_rectangle_lines_ex(self.rect, 1, pr.RED)

    def update(self) -> None:
        if pr.check_collision_point_rec(pr.get_mouse_position(), self.rect):
            self.current_color = self.highlighted_color
            if pr.is_mouse_button_pressed(0):
                print(
                    f"{self.text}, {pr.check_collision_point_rec(pr.get_mouse_position(), self.rect)}, {pr.is_mouse_button_pressed(0)}"
                )
                self.state_changed = not self.state_changed
                self.is_clicked = True
        else:
            self.current_color = self.font_color

    def has_been_clicked(self) -> bool:
        return self.is_clicked
