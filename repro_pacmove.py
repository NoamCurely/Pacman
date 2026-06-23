import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import random
import pygame
pygame.init()
pygame.display.set_mode((1, 1))

from src.game.maze import Maze
from src.game.pacman import Pacman
from src.game.directions import DIRECTIONS

grids = [(21, 21), (29, 27), (35, 31), (39, 35)]
RESOLUTIONS = [(1920, 1080), (1366, 768), (1280, 1024)]
SNAP = 6  # how close to center before re-picking a direction

for sw, sh in RESOLUTIONS:
    hud_h = round(sh * 40 / 720)
    area = pygame.Rect(0, 0, sw, sh - hud_h)
    for w, h in grids:
        maze = Maze(w, h, seed=42)
        cell = maze.cell_size(area)
        size = max(8, int(cell * 0.9))
        pac = Pacman(area)
        pac.resize(size)
        x, y = maze.find_open_cell(area)
        pac.pos = pygame.Vector2(x, y)
        rng = random.Random(1)
        max_stall = 0
        stall = 0
        last_cell = None
        for _ in range(6000):
            col, row = maze.cell_at(pac.pos.x, pac.pos.y, area)
            cx, cy = maze.cell_center(col, row, area)
            near = abs(pac.pos.x - cx) <= SNAP and abs(pac.pos.y - cy) <= SNAP
            if near:
                opts = [n for n, (dx, dy) in DIRECTIONS.items()
                        if not maze.is_wall(cx, cy, dx * cell, dy * cell, area)]
                if opts:
                    pac.queued_dir = rng.choice(opts)
            pac.update(maze, area)
            cur = maze.cell_at(pac.pos.x, pac.pos.y, area)
            if cur == last_cell:
                stall += 1
                max_stall = max(max_stall, stall)
            else:
                stall = 0
                last_cell = cur
        flag = "  <-- STUCK" if max_stall > 200 else ""
        print(f"{sw}x{sh} {w}x{h} cell {cell:2} spr {size:2} "
              f"max_stall {max_stall:4} frames{flag}")
    print()
