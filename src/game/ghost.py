"""Ghost entity: pathfinding, chase/flee behaviour and rendering."""
import random
import pygame

from src.game.maze import Maze
from src.game.directions import DIRECTIONS as DIRS, OPPOSITE
from src.game.spritesheet import SpriteSheet, load_ghost, load_frightened
from src.game.algo import Algo

GHOST_SIZE = 32
RNG = random.Random()
DEAD_MS = 5000

Cell = tuple[int, int]


class Ghost:
    """A single ghost with its sprites, position and AI state."""

    def __init__(self, maze: Maze, name: str, speed: float) -> None:
        self.maze = maze
        self.name = name
        self.speed = speed
        self.sheet = SpriteSheet()
        self.algo = Algo
        self._raw_frames = load_ghost(self.sheet, name)
        self._raw_fright = load_frightened(self.sheet)
        self.frames: dict[str, list[pygame.Surface]] = {}
        self.fright: dict[str, list[pygame.Surface]] = {}
        self.size = GHOST_SIZE
        self.resize(GHOST_SIZE)
        self.direction = "right"
        self.frame_idx = 0
        self.spawn_cell: Cell = (0, 0)
        self.pos = pygame.Vector2(0, 0)
        self.dir: Cell = (0, 0)
        self._last_cell: Cell | None = None
        self.frightened = False
        self.fright_until = 0
        self.dead = False
        self.dead_until = 0
        self.freeze = False

    def resize(self, size: int) -> None:
        """Rescale ghost sprites to the given pixel size (one maze cell)."""
        self.size = size
        self.frames = {
            d: [SpriteSheet.scale(f, size) for f in fs]
            for d, fs in self._raw_frames.items()
        }
        self.fright = {
            k: [SpriteSheet.scale(f, size) for f in fs]
            for k, fs in self._raw_fright.items()
        }

    def reset(self, area: pygame.Rect) -> None:
        """Move the ghost back to its spawn cell and clear dead state."""
        cx, cy = self.maze.cell_center(*self.spawn_cell, area)
        self.pos = pygame.Vector2(cx, cy)
        self.dead = False
        self.dead_until = 0
        self.dir = (0, 0)
        self._last_cell = None

    def set_frightened(self, duration_ms: int = 7000) -> None:
        """Make the ghost edible for the given duration."""
        self.frightened = True
        self.fright_until = pygame.time.get_ticks() + duration_ms

    def eaten(self) -> None:
        """Mark the ghost as eaten and start its respawn timer."""
        self.frightened = False
        self.dir = (0, 0)
        self.dead = True
        self.dead_until = pygame.time.get_ticks() + DEAD_MS

    def flee_dir(self, area: pygame.Rect) -> str | None:
        """Return a random open direction, avoiding a U-turn when possible."""
        exits = self.open_dirs(area)
        if not exits:
            return None
        back = OPPOSITE[self.direction]
        if len(exits) > 1 and back in exits:
            exits = [d for d in exits if d != back]
        return RNG.choice(exits)

    def open_dirs(self, area: pygame.Rect) -> list[str]:
        """Return the direction names not blocked by a wall."""
        cx, cy = self.pos.x, self.pos.y
        step = self.maze.cell_size(area)
        exits = []
        for name, (dx, dy) in DIRS.items():
            if not self.maze.is_wall(cx, cy, dx * step, dy * step, area):
                exits.append(name)
        return exits

    def astar_dir(
        self,
        maze: Maze,
        area: pygame.Rect,
        start_cell: Cell,
        goal_cell: Cell,
    ) -> str | None:
        """Return the first step direction of the A* path, if any."""
        path = self.algo.astar(maze, area, start_cell, goal_cell)
        if len(path) < 2:
            return None
        next_cell = path[1]
        dx = next_cell[0] - start_cell[0]
        dy = next_cell[1] - start_cell[1]
        for name, vec in DIRS.items():
            if vec == (dx, dy):
                return name
        return None

    def target_cell(self, pac_cell: Cell, pac_dir: str) -> Cell:
        """Return the chase target cell for this ghost's personality."""
        if self.name == "pinky":
            dx, dy = DIRS.get(pac_dir, (0, 0))
            return (pac_cell[0] + dx * 4, pac_cell[1] + dy * 4)
        if self.name == "inky":
            return (pac_cell[0] + 2, pac_cell[1] + 2)
        if self.name == "clyde":
            return (pac_cell[0] - 2, pac_cell[1] - 2)
        return pac_cell

    def update(
        self,
        maze: Maze,
        area: pygame.Rect,
        pac_cell: Cell,
        pac_dir: str,
    ) -> None:
        """Advance the ghost: pick a direction at cell centers and move."""
        if self.freeze:
            return
        if self.frightened and pygame.time.get_ticks() >= self.fright_until:
            self.frightened = False
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
        ghost_cell = maze.cell_at(self.pos.x, self.pos.y, area)

        # Re-decide at every cell center, and also whenever stopped, so a
        # ghost can never get stuck: dir=(0,0) is not a terminal state.
        if center and (ghost_cell != self._last_cell or self.dir == (0, 0)):
            self.pos.update(cx, cy)
            self._last_cell = ghost_cell
            if self.frightened:
                choice = self.flee_dir(area)
            else:
                goal = self.target_cell(pac_cell, pac_dir)
                choice = self.astar_dir(maze, area, ghost_cell, goal)
                if choice is None:
                    choice = self.astar_dir(maze, area, ghost_cell, pac_cell)
            # astar returns no step when the ghost sits on its target (e.g.
            # on top of an invincible Pacman); keep roaming via any open exit
            # instead of freezing forever.
            if choice is None:
                choice = self.flee_dir(area)
            if choice is not None:
                self.direction = choice
                self.dir = DIRS[choice]
            else:
                self.dir = (0, 0)

        dx, dy = self.dir
        self.pos.x += dx * self.speed
        self.pos.y += dy * self.speed

    def draw(self, screen: pygame.Surface, area: pygame.Rect) -> None:
        """Blit the current ghost sprite (normal or frightened)."""
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
