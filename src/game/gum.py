from src.game.maze import Maze
from src.parsing import Config


class Gum:
    def __init__(self, maze: Maze, config: Config) -> None:
        self.gum = set[tuple[int, int]] = set()
        self.super_gum = set[tuple[int, int]] = set()
        self.place(maze, config)

    def cornes_cell(self, maze: Maze):
        pass

    def place(self, maze: Maze, config: Config):
        corners = self.cornes_cell(maze)
        for y in range(maze.rows):
            for x in range(maze.cols):
                cell = (x, y)
                if maze.grid[y][x] == 15:
                    continue
                if maze.is_wall(cell):
                    continue
                if cell in self.ghost_spawn:
                    continue
                if cell in corners:
                    self.super_gum.add(cell)
                elif:
                    self.gum.add(cell)

    def eat(self, cell) -> int:
        pass

    def remaining(self) -> int:
        pass

    def draw(self, screen, area, cell_size, sprites):
        pass

    