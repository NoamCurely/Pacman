import heapq
import random
import pygame

from src.game.maze import Maze
from src.game.directions import DIRECTIONS as DIRS
from src.game.spritesheet import SpriteSheet, load_ghost, load_frightened

GHOST_SIZE = 32
RNG = random.Random()


def neighbors(maze, area, cell):
    col, row = cell
    cx, cy = maze.cell_center(col, row, area)
    step = maze.cell_size(area)
    result = []
    for dx, dy in DIRS.values():
        if not maze.is_wall(cx, cy, dx * step, dy * step, area):
            result.append((col + dx, row + dy))
    return result


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze, area, start, goal):
    count = 0
    open_heap = [(manhattan(start, goal), count, start)]
    came_from = {}
    g = {start: 0}

    while open_heap:
        _, _, current = heapq.heappop(open_heap)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
        for nb in neighbors(maze, area, current):
            tentative = g[current] + 1
            if nb not in g or tentative < g[nb]:
                g[nb] = tentative
                came_from[nb] = current
                count += 1
                f = tentative + manhattan(nb, goal)
                heapq.heappush(open_heap, (f, count, nb))
    return []


class Ghost:

    def __init__(self, maze: Maze, name: str, speed: float) -> None:
        self.maze = maze
        self.name = name
        self.speed = speed
        self.sheet = SpriteSheet()
        raw = load_ghost(self.sheet, name)
        self.frames = {
            d: [SpriteSheet.scale(f, GHOST_SIZE) for f in fs]
            for d, fs in raw.items()
        }
        fr = load_frightened(self.sheet)
        self.fright = {
            k: [SpriteSheet.scale(f, GHOST_SIZE) for f in fs]
            for k, fs in fr.items()
        }
        self.direction = "right"
        self.frame_idx = 0
        self.spawn_cell: tuple[int, int] = (0, 0)
        self.pos = pygame.Vector2(0, 0)
        self.dir: tuple[int, int] = (0, 0)
        self.frightened = False
        self.fright_until = 0
        self.dead = False
        self.dead_until = 0

    def reset(self, area: pygame.Rect) -> None:
        cx, cy = self.maze.cell_center(*self.spawn_cell, area)
        self.pos = pygame.Vector2(cx, cy)
        self.dead = False
        self.dead_until = 0
        self.dir = (0, 0)

    def set_frightened(self, duration_ms: int = 7000) -> None:
        self.frightened = True
        self.fright_until = pygame.time.get_ticks() + duration_ms

    DEAD_MS = 5000

    def eaten(self, area: pygame.Rect) -> None:
        self.frightened = False
        self.dir = (0, 0)
        self.dead = True
        self.dead_until = pygame.time.get_ticks() + self.DEAD_MS

    def flee_dir(self, area: pygame.Rect) -> str | None:
        exits = self.open_dirs(area)
        if not exits:
            return None
        opposite = {"up": "down", "down": "up",
                    "left": "right", "right": "left"}
        back = opposite[self.direction]
        if len(exits) > 1 and back in exits:
            exits = [d for d in exits if d != back]
        return RNG.choice(exits)

    def open_dirs(self, area):
        cx, cy = self.pos.x, self.pos.y
        step = self.maze.cell_size(area)
        exits = []
        for name, (dx, dy) in DIRS.items():
            if not self.maze.is_wall(cx, cy, dx * step, dy * step, area):
                exits.append(name)
        return exits

    def astar_dir(self, maze, area, start_cell, goal_cell):
        path = astar(maze, area, start_cell, goal_cell)
        if len(path) < 2:
            return None
        next_cell = path[1]
        dx = next_cell[0] - start_cell[0]
        dy = next_cell[1] - start_cell[1]
        for name, vec in DIRS.items():
            if vec == (dx, dy):
                return name
        return None

    def target_cell(self, pac_cell, pac_dir):
        if self.name == "pinky":
            dx, dy = DIRS.get(pac_dir, (0, 0))
            return (pac_cell[0] + dx * 4, pac_cell[1] + dy * 4)
        if self.name == "inky":
            return (pac_cell[0] + 2, pac_cell[1] + 2)
        if self.name == "clyde":
            return (pac_cell[0] - 2, pac_cell[1] - 2)
        return pac_cell

    def update(self, maze: Maze, area: pygame.Rect,
               pac_cell, pac_dir) -> None:
        if self.dead:
            if pygame.time.get_ticks() >= self.dead_until:
                self.reset(area)
            return
        if self.frightened and pygame.time.get_ticks() >= self.fright_until:
            self.frightened = False
        cx, cy = maze.cell_center(
            *maze.cell_at(self.pos.x, self.pos.y, area), area)
        center = (abs(self.pos.x - cx) < self.speed
                  and abs(self.pos.y - cy) < self.speed)

        if center:
            self.pos.update(cx, cy)
            ghost_cell = maze.cell_at(self.pos.x, self.pos.y, area)
            if self.frightened:
                choice = self.flee_dir(area)
            else:
                goal = self.target_cell(pac_cell, pac_dir)
                choice = self.astar_dir(maze, area, ghost_cell, goal)
                if choice is None:
                    choice = self.astar_dir(maze, area, ghost_cell, pac_cell)
            if choice is not None:
                self.direction = choice
                self.dir = DIRS[choice]
            else:
                self.dir = (0, 0)

        dx, dy = self.dir
        self.pos.x += dx * self.speed
        self.pos.y += dy * self.speed

    def draw(self, screen: pygame.Surface, area: pygame.Rect) -> None:
        if self.dead:
            return
        if self.frightened:
            remaining = self.fright_until - pygame.time.get_ticks()
            key = "blue"
            if remaining < 1000 and (remaining // 200) % 2 == 0:
                key = "white"
            spr = self.fright[key][self.frame_idx % 2]
        else:
            spr = self.frames[self.direction][self.frame_idx]
        rect = spr.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(spr, rect)
