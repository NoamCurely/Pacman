"""Gum: placement, eating and rendering of pacgums and super-pacgums."""
import random

import pygame

from src.game.maze import Maze
from src.parsing import Config

GUM_COLOR = (255, 184, 151)
SUPER_COLOR = (255, 230, 180)


class Gum:
    """Track and draw the pacgums and super-pacgums of a level."""

    def __init__(
        self,
        maze: Maze,
        config: Config,
        ghost_spawns: set[tuple[int, int]],
        player_spawn: tuple[int, int]
    ) -> None:
        self.gum: set[tuple[int, int]] = set()
        self.super_gum: set[tuple[int, int]] = set()
        self.ghost_spawns = ghost_spawns
        self.player_spawn = player_spawn
        self.points_pacgum = config.points_per_pacgum
        self.points_super = config.points_per_super_pacgum
        self.place(maze, config)

    def place(self, maze: Maze, config: Config) -> None:
        """Put super-pacgums in corners and pacgums on random cells."""
        corners = maze.corner_cells()
        skip = self.ghost_spawns | {self.player_spawn}

        candidates = []
        for y in range(maze.rows):
            for x in range(maze.cols):
                cell = (x, y)
                if maze.grid[y][x] == 15:
                    continue
                if cell in corners:
                    self.super_gum.add(cell)
                    continue
                if cell in skip:
                    continue
                candidates.append(cell)

        wanted_count = min(config.pacgum, len(candidates))
        picker = random.Random(config.seed)
        self.gum = set(picker.sample(candidates, wanted_count))

    def eat(self, cell: tuple[int, int]) -> int:
        """Eat the gum at cell and return the points scored."""
        if cell in self.gum:
            self.gum.discard(cell)
            return self.points_pacgum
        if cell in self.super_gum:
            self.super_gum.discard(cell)
            return self.points_super
        return 0

    def remaining(self) -> int:
        """Return the number of pacgums left."""
        return len(self.gum)

    def draw(self, screen: pygame.Surface, area: pygame.Rect,
             maze: Maze) -> None:
        """Draw all remaining pacgums and super-pacgums."""
        size = maze.cell_size(area)
        r = max(2, size // 10)
        big_r = max(4, size // 6)
        for col, row in self.gum:
            cx, cy = maze.cell_center(col, row, area)
            pygame.draw.circle(screen, GUM_COLOR, (cx, cy), r)
        for col, row in self.super_gum:
            cx, cy = maze.cell_center(col, row, area)
            pygame.draw.circle(screen, SUPER_COLOR, (cx, cy), big_r)
