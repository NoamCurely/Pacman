import heapq

import pygame

from src.game.maze import Maze
from src.game.directions import DIRECTIONS as DIRS


Cell = tuple[int, int]


class Algo:
    @staticmethod
    def neighbors(maze: Maze, area: pygame.Rect, cell: Cell) -> list[Cell]:
        """Return the walkable cells adjacent to cell."""
        col, row = cell
        cx, cy = maze.cell_center(col, row, area)
        step = maze.cell_size(area)
        result = []
        for dx, dy in DIRS.values():
            if not maze.is_wall(cx, cy, dx * step, dy * step, area):
                result.append((col + dx, row + dy))
        return result

    @staticmethod
    def manhattan(a: Cell, b: Cell) -> int:
        """Return the Manhattan distance between two cells."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def astar(
        maze: Maze,
        area: pygame.Rect,
        start: Cell,
        goal: Cell,
    ) -> list[Cell]:
        """Return the shortest cell path from start to goal via A*."""
        count = 0
        open_heap = [(Algo.manhattan(start, goal), count, start)]
        came_from: dict[Cell, Cell] = {}
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
            for nb in Algo.neighbors(maze, area, current):
                tentative = g[current] + 1
                if nb not in g or tentative < g[nb]:
                    g[nb] = tentative
                    came_from[nb] = current
                    count += 1
                    f = tentative + Algo.manhattan(nb, goal)
                    heapq.heappush(open_heap, (f, count, nb))
        return []
