import pygame

from mazegenerator import MazeGenerator

WALL_COLOR = (33, 33, 222)
WALL_W = 4


class Maze:
    def __init__(self, width: int, height: int, seed: int = 0) -> None:
        gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        self.grid: list[list[int]] = gen.maze
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def draw(self, screen: pygame.Surface) -> None:
        screen_w, screen_h = screen.get_size()
        cell_size = min(screen_w // self.cols, screen_h // self.rows)
        offset_x = (screen_w - self.cols * cell_size) // 2
        offset_y = (screen_h - self.rows * cell_size) // 2

        for y in range(self.rows):
            for x in range(self.cols):
                v = self.grid[y][x]
                left = offset_x + x * cell_size
                top = offset_y + y * cell_size
                right, bottom = left + cell_size, top + cell_size
                north = v & 1
                east = v & 2
                south = v & 4
                west = v & 8

                if north:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (left, top), (right, top), WALL_W)
                if east:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (right, top), (right, bottom), WALL_W)
                if south:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (left, bottom), (right, bottom), WALL_W)
                if west:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (left, top), (left, bottom), WALL_W)
