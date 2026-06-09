"""Spawn: compute the player and ghost spawn cells of a maze."""
import random

from src.game.maze import Maze
from src.game.ghost import Ghost


class Spawn:
    """Compute spawn cells for the player and the ghosts."""

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def ghost_spawns(self) -> list[tuple[int, int]]:
        """Return the four corner cells each moved one step inward."""
        cx, cy = self.maze.cols // 2, self.maze.rows // 2
        cells = []
        for corner_x, corner_y in self.maze.corner_cells():
            dx = (cx > corner_x) - (cx < corner_x)
            dy = (cy > corner_y) - (cy < corner_y)
            cells.append((corner_x + dx, corner_y + dy))
        return cells

    def random_ghost(self, ghosts: list[Ghost]) -> None:
        """Assign each ghost a random spawn cell using an independent RNG."""
        cells = self.ghost_spawns()
        rng = random.Random()
        rng.shuffle(cells)
        for ghost, cell in zip(ghosts, cells):
            ghost.spawn_cell = cell
