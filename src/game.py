import asyncio
import pyray as pr


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

    def update(self) -> None:
        pass

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
            await asyncio.sleep(0)

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        pr.draw_fps(0,0)
        pr.end_drawing()

    def end(self) -> None:
        pr.close_window()
