import asyncio
from pathlib import Path

import pyray as pr

from src.game import Game
from src.resource_manager import ResourceManager

THIS_DIR = (Path(__file__).parent / "src").resolve()


async def main() -> None:
    resources_manager = ResourceManager(resources_path=f"{THIS_DIR}/resources.json")
    game = Game(resources_manager=resources_manager)
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
