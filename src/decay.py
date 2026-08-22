import random
import math
import pyray as pr

width, height = 600, 600


class Remnant:
    """
    - class to create a single remnant after an explosion has been issued
    - remnant is moving straight given a speed and direction
    """

    def __init__(
        self,
        id: int,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        lifetime: int,
        color: pr.Color,
    ) -> None:
        self.id = id
        self.x = position.x
        self.y = position.y
        self.dx = direction.x
        self.dy = direction.y
        self.width = width
        self.height = height
        self.speed = speed
        self.lifetime: int = lifetime
        self.color = color
        self.angle = math.degrees(math.atan2(self.dy, self.dx))
        self.creation_time = pr.get_time()
        self.discard = False

    def update(self, dt: float) -> None:
        if pr.get_time() - self.creation_time > self.lifetime:
            self.discard = True
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

    def draw(self) -> None:
        center = pr.Vector2(0, 0)
        tmp_rect = pr.Rectangle(self.x, self.y, self.width, self.height)
        pr.draw_rectangle_pro(tmp_rect, center, self.angle, self.color)

    def __repr__(self) -> str:
        return f"id: {self.id}, dir: ({self.dx}, {self.dy}), speed:{self.speed}, w,h: ({self.width, self.height}), angle: {self.angle}"


class Decay:
    """
    - class to implement an 'explosion' animation with pyray primitive shape
    - The idea is that at the spawn point: `position`, `children` small asteroid remants are emitted with a `max_size`
    - Children have different directions (and velocities ?)
    - TO DO: add a timer after which the remants are disable
    """

    def __init__(
        self,
        position: pr.Vector2,
        max_size: pr.Vector2,
        children: int,
        speed: int,
        lifetime: int,
        color: pr.Color,
    ) -> None:
        self.position = position  # position where the Explosion is spawned
        self.max_size = max_size  # array if (min, max) values for the remnants
        self.children = children  # number of remnants
        self.speed = speed  # speed of the remnant
        self.lifetime = lifetime  # life time of the remnant, ie. after lifetime, the remnants is discarded
        self.color = color  # color of the remnant
        self.remnants: list[Remnant] = self.create_children()

    def create_children(self) -> list[Remnant]:
        tmp = []
        for i in range(0, self.children):
            width = random.randint(int(self.max_size.x), int(self.max_size.y))
            height = random.randint(int(self.max_size.x), int(self.max_size.y))
            direction = pr.Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
            # normalize direction (avoid zero-length)
            length = math.hypot(direction.x, direction.y)
            if length == 0:
                direction = pr.Vector2(1, 0)
                length = 1
            direction = pr.Vector2(direction.x / length, direction.y / length)
            speed = random.randint(self.speed//4, self.speed//2)
            tmp.append(
                Remnant(
                    id=i,
                    position=self.position,
                    direction=direction,
                    width=width,
                    height=height,
                    speed=speed,
                    lifetime=self.lifetime,
                    color=self.color,
                )
            )
        return tmp

    def update(self, dt: float) -> None:
        _ = [remnant.update(dt) for remnant in self.remnants]

    def draw(self) -> None:
        _ = [remnant.draw() for remnant in self.remnants if not remnant.discard]

    def debug(self) -> None:
        print(f"created {self.children} mini asteroids")
        _ = [print(remnant) for remnant in self.remnants]