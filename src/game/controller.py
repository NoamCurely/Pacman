import pygame
from src.game.maze import Maze
from src.game.spritesheet import SpriteSheet, load_pacman_dir


class Controller:
    FRAME_MS = 200
    SPEED = 2.5
    SNAP_THRESHOLD = SPEED + 6
    VECTORS = {
        'right': (1, 0),
        'left': (-1, 0),
        'up': (0, -1),
        'down': (0, 1),
    }

    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.screen_rect = screen_rect
        self.sheet = SpriteSheet()
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
        if (event.type == pygame.KEYDOWN):
            if (event.key in self.keymap):
                self.queued_dir = self.keymap[event.key]

    def change_dir(self, direction: str) -> None:
        self.direction = direction
        raw_frames = load_pacman_dir(self.sheet, direction)
        self.frames = [SpriteSheet.scale(f, 32) for f in raw_frames]
        self.frame_idx = 0
        self.vel = pygame.Vector2(self.VECTORS[direction]) * self.SPEED

    def update(self, maze: Maze, maze_area: pygame.Rect) -> None:
        now = pygame.time.get_ticks()
        if (now - self.last_tick >= self.FRAME_MS):
            self.frame_idx = (self.frame_idx + 1) % len(self.frames)
            self.last_tick = now

        cell_size = min(maze_area.width // maze.cols,
                        maze_area.height // maze.rows)

        offset_x = maze_area.x + (
            maze_area.width - maze.cols * cell_size) // 2
        offset_y = maze_area.y + (
            maze_area.height - maze.rows * cell_size) // 2

        col = int((self.pos.x - offset_x) // cell_size)
        row = int((self.pos.y - offset_y) // cell_size)
        cell_cx = offset_x + col * cell_size + cell_size // 2
        cell_cy = offset_y + row * cell_size + cell_size // 2

        on_grid = (abs(self.pos.x - cell_cx) <= self.SNAP_THRESHOLD and
                   abs(self.pos.y - cell_cy) <= self.SNAP_THRESHOLD)

        if (self.vel.x != 0):
            self.pos.y = cell_cy

        if (self.vel.y != 0):
            self.pos.x = cell_cx

        if (self.queued_dir and on_grid):
            vx, vy = self.VECTORS[self.queued_dir]
            cand = pygame.Vector2(vx, vy) * self.SPEED
            if not self._blocked(maze, maze_area, cand):
                self.change_dir(self.queued_dir)
                self.queued_dir = None

        if not self._blocked(maze, maze_area, self.vel):
            self.pos += self.vel

    def _blocked(self, maze: Maze, maze_area: pygame.Rect,
                 vel: pygame.Vector2) -> bool:
        """True si avancer de `vel` depuis la position courante tape un mur."""
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

    def move(self, dx: int, dy: int) -> None:
        self.frame_idx = 0

    @property
    def pac(self) -> pygame.Surface:
        return self.frames[self.frame_idx]

    keymap = {
        pygame.K_UP: 'up',
        pygame.K_DOWN: 'down',
        pygame.K_LEFT: 'left',
        pygame.K_RIGHT: 'right',
    }
