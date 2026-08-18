import asyncio
import random
import PolygonCollision

import pyray as pr

from .resource_manager import ResourceManager
from src.entity import Entity
from src.projectile import Projectile


class Game:
    def __init__(self, resources_manager) -> None:
        self.resources_manager: ResourceManager = resources_manager
        self.width: int = self.resources_manager.game_data().get("width")
        self.height: int = self.resources_manager.game_data().get("height")
        self.fps_target: int = self.resources_manager.game_data().get("fps")
        self.background_color: pr.Color = tuple(
            self.resources_manager.game_data().get("background_color")
        )
        self.name: str = self.resources_manager.game_data().get("name")
        self.debug: bool = self.resources_manager.game_data().get("debug")
        self.projectile_data = self.resources_manager.projectile()

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.entity = Entity(
            position=pr.Vector2(self.width // 2, self.height // 2),
            inner_radius=self.resources_manager.entity().get("inner_radius"),
            outer_radius=self.resources_manager.entity().get("outer_radius"),
            guard_inner_radius=self.resources_manager.entity().get("guard_inner_radius"),
            guard_outer_radius=self.resources_manager.entity().get("guard_outer_radius"),
            inner_color=self.resources_manager.entity().get("inner_color"),
            outer_color=self.resources_manager.entity().get("outer_color"),
        )
        self.projectiles: list[Projectile] = []

    def check_collisions_neutrons_shield(self) -> None:
        for proj in self.projectiles:
            proj_rect = proj.get_rectangle()
            shield_rect = self.entity.get_shield().get_rectangle()

            proj_polygon = PolygonCollision.shape.Shape(
                vertices=[tuple([r.x, r.y]) for r in proj_rect]
            )
            shield_polygon = PolygonCollision.shape.Shape(
                vertices=[tuple([r.x, r.y]) for r in shield_rect]
            )
            if proj_polygon.collide(shield_polygon):
                print(f"COLLISION between :{proj_polygon} and {shield_polygon}")
                proj.direction.x *= -1
                proj.direction.y *= -1
                break

    def check_collisions(self) -> None:
        for proj in self.projectiles:
            if pr.check_collision_circles(
                self.entity.position,
                self.entity.outer_radius,
                proj.position,
                proj.radius,
            ):
                print("collision")
                self.entity.inner_radius += proj.radius
                self.entity.outer_radius += proj.radius
                proj.is_disabled = True
                break
        self.projectiles = [proj for proj in self.projectiles if not proj.is_disabled]

    def update(self) -> None:
        # input
        dt = pr.get_frame_time()

        # check collisions
        # self.check_collisions()
        self.check_collisions_neutrons_shield()

        # update entity
        self.entity.update(dt=dt)

        # update projectiles
        _ = [proj.update(dt) for proj in self.projectiles if not proj.is_disabled]

    async def run(self) -> None:
        while not pr.window_should_close():
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                mouse_pos: pr.Vector2 = pr.get_mouse_position()
                self.projectiles.append(
                    Projectile(
                        position=mouse_pos,  # instantiate the ring where the mouse is clicked
                        direction=pr.Vector2(
                            random.uniform(self.projectile_data.get("direction")[0], self.projectile_data.get("direction")[1]), 
                            random.uniform(self.projectile_data.get("direction")[0], self.projectile_data.get("direction")[1])),  
                        speed=random.randint(self.projectile_data.get("speed")[0], self.projectile_data.get("speed")[1]),  # random speed in [400, 600]
                        radius=random.randint(self.projectile_data.get("radius")[0], self.projectile_data.get("radius")[1]),  # random radius
                        color=self.projectile_data.get("color"),
                        game_window=pr.Vector2(self.width, self.height),
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
        _ = [proj.draw() for proj in self.projectiles if not proj.is_disabled]
        pr.draw_fps(0, 0)
        pr.draw_text(f"FRAME TIME: {int(1000*pr.get_frame_time())}ms", 0, 20, 20, pr.DARKGREEN)
        pr.draw_text(f"PROJECTILES:{len(self.projectiles)}", 0, 40, 20, pr.DARKGREEN)
        pr.draw_line_v(
            pr.Vector2(0, self.height // 2),
            pr.Vector2(self.width, self.height // 2),
            pr.DARKGREEN,
        )
        pr.draw_line_v(
            pr.Vector2(self.width // 2, 0),
            pr.Vector2(self.width // 2, self.height),
            pr.DARKGREEN,
        )
        pr.end_drawing()

    def end(self) -> None:
        pr.close_window()
