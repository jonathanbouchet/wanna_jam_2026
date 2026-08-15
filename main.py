import asyncio
from src.game import Game
import pyray as pr

async def main() -> None:
    game = Game(
        width=600, height=600, fps_target=60, name="app", background_color=pr.BLACK
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())