import asyncio
import random
import pyray as pr
from src.entity import Entity
from src.projectile import Projectile


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.entity = Entity(position=pr.Vector2(self.width//2, self.height//2), inner_radius= 50, outer_radius=70, inner_color=pr.RED, outer_color=pr.PINK)
        self.projectiles: list[Projectile] = []

    def update(self) -> None:
        # input
        dt = pr.get_frame_time()
        _ = [r.update(dt) for r in self.projectiles]

    async def run(self) -> None:
        while not pr.window_should_close():
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                player_pos: pr.Vector2 = pr.get_mouse_position()
                self.projectiles.append(
                    Projectile(
                        position=player_pos,  # instantiate the ring where the mouse is clicked
                        direction=pr.Vector2(
                            random.uniform(-1, 1), random.uniform(-1, 1)
                        ),  # random direction
                        speed=random.randint(400, 600),  # random speed in [400, 600]
                        radius=random.randint(10, 15),  # random radius
                        color=pr.DARKGRAY,  # random color
                        game_window=pr.Vector2(self.width, self.height)
                    )
                )
                print(self.projectiles[-1])
            self.update()
            self.draw()
            await asyncio.sleep(0)

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        self.entity.draw()
        _ = [r.draw() for r in self.projectiles]
        pr.draw_fps(0,0)
        pr.draw_line_v(pr.Vector2(0, self.height//2), pr.Vector2(self.width, self.height//2), pr.DARKGREEN)
        pr.draw_line_v(pr.Vector2(self.width//2, 0), pr.Vector2(self.width//2, self.height), pr.DARKGREEN)
        pr.end_drawing()

    def end(self) -> None:
        pr.close_window()
