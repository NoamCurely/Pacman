"""Controller: player movement, animation and wall collision."""
import pygame

from src.game.maze import Maze
from src.game.directions import DIRECTIONS as VECTORS
from src.game.spritesheet import SpriteSheet, load_pacman

FRAME_MS = 200
SPEED = 2.5
SNAP_THRESHOLD = SPEED + 6


class Controller:
    """Drive a sprite through the maze from keyboard input."""

    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.screen_rect = screen_rect
        self.sheet = SpriteSheet()
        self.frames_by_dir = {
            d: [SpriteSheet.scale(f, 32) for f in fs]
            for d, fs in load_pacman(self.sheet).items()
        }
        self.direction = 'right'
        self.queued_dir: str | None = None
        self.frames: list[pygame.Surface] = []
        self.frame_idx = 0
        self.last_tick = pygame.time.get_ticks()
        self.vel = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(
            screen_rect.centerx,
            screen_rect.centery,
        )
        self.change_dir('right')

    def handle_event(self, event: pygame.event.Event) -> None:  
        """Queue a direction change from a key press."""
        if (event.type == pygame.KEYDOWN):
            if (event.key in self.keymap):
                self.queued_dir = self.keymap[event.key]

    def change_dir(self, direction: str) -> None:
        """Switch to direction, resetting the animation and velocity."""
        self.direction = direction
        self.frames = self.frames_by_dir[direction]
        self.frame_idx = 0
        self.vel = pygame.Vector2(VECTORS[direction]) * SPEED

    def update(
        self,
        maze: Maze,
        maze_area: pygame.Rect,
        noclip: bool = False
    ) -> None:
        """Advance animation and move, snapping and turning on the grid."""
        now = pygame.time.get_ticks()
        if (now - self.last_tick >= FRAME_MS):
            self.frame_idx = (self.frame_idx + 1) % len(self.frames)
            self.last_tick = now

        col, row = maze.cell_at(self.pos.x, self.pos.y, maze_area)
        cell_cx, cell_cy = maze.cell_center(col, row, maze_area)

        on_grid = (abs(self.pos.x - cell_cx) <= SNAP_THRESHOLD and
                   abs(self.pos.y - cell_cy) <= SNAP_THRESHOLD)

        if (self.vel.x != 0):
            self.pos.y = cell_cy

        if (self.vel.y != 0):
            self.pos.x = cell_cx

        blocked_now = self._blocked(maze, maze_area, self.vel)
        if self.queued_dir and (on_grid or blocked_now):
        #if (self.queued_dir and on_grid):
            vx, vy = VECTORS[self.queued_dir]
            cand = pygame.Vector2(vx, vy) * SPEED
            if noclip or not self._blocked(maze, maze_area, cand):
                self.change_dir(self.queued_dir)
                self.queued_dir = None

        if noclip or not self._blocked(maze, maze_area, self.vel):
            self.pos += self.vel

    def _blocked(
        self,
        maze: Maze,
        maze_area: pygame.Rect,
        vel: pygame.Vector2
    ) -> bool:
        """Return True if moving by vel would push a corner into a wall."""
        half = self.pac.get_width() // 2 - 1
        corners = [
            (-half, -half),
            (half, -half),
            (-half, half),
            (half, half),
        ]
        return any(
            maze.is_wall(
                self.pos.x + cx, self.pos.y + cy,
                vel.x, vel.y,
                maze_area
            )
            for cx, cy in corners
        )

    @property
    def pac(self) -> pygame.Surface:
        """Return the current animation frame surface."""
        return self.frames[self.frame_idx]

    keymap = {
        pygame.K_UP: 'up',
        pygame.K_DOWN: 'down',
        pygame.K_LEFT: 'left',
        pygame.K_RIGHT: 'right',
    }
