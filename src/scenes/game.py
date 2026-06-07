import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene
from src.ui.hud import Hud
from src.game.maze import Maze, BG_COLOR
from src.game.pacman import Pacman
from src.game.gum import Gum
from src.game.ghost import Ghost
from src.game.spawn import Spawn
from src.sounds import sfx


class Game(Scene):
    """Scène de jeu: labyrinthe du niveau courant + bandeau HUD en bas."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        level = config.levels[0]
        self.maze = Maze(level.width, level.height, seed=config.seed)

        h = screen_rect.height
        hud_h = round(h * 40 / 720)
        self.maze_area = pygame.Rect(
            0, 0, screen_rect.width, h - hud_h)
        self.hud_area = pygame.Rect(
            0, h - hud_h, screen_rect.width, hud_h)
        self.hud = Hud(fonts, self.hud_area)

        self.score = 0
        self.lives = config.lives
        self.time_left = config.level_max_time
        self.pacman = Pacman(self.maze, config, self.maze_area)
        sx, sy = self.maze.find_open_cell(self.maze_area)
        self.pacman.pos = pygame.Vector2(sx, sy)
        spawn_cell = self.maze.cell_at(sx, sy, self.maze_area)

        self.spawn = Spawn(self.maze)
        ghost_cells = set(self.spawn.ghost_spawns())
        self.gum = Gum(self.maze, config, ghost_cells, spawn_cell)

        self.ghosts = [Ghost(self.maze, name)
                       for name in ("blinky", "pinky", "inky", "clyde")]
        self.spawn.random_ghost(self.ghosts)
        for ghost in self.ghosts:
            ghost.reset(self.maze_area)

        sfx.play("pacman_beginning.wav")

    def update(self) -> None:
        self.pacman.update(self.maze, self.maze_area)
        cell = self.maze.cell_at(
            self.pacman.pos.x,
            self.pacman.pos.y,
            self.maze_area
        )
        for ghost in self.ghosts:
            ghost.update(self.maze, self.maze_area, cell,
                         self.pacman.direction)
        is_super = cell in self.gum.super_gum
        gained = self.gum.eat(cell)
        self.score += gained
        if is_super:
            sfx.play("pacman_eatfruit.wav")
            for ghost in self.ghosts:
                ghost.set_frightened()
        elif gained > 0:
            sfx.play("pacman_chomp.wav")

        for ghost in self.ghosts:
            gcell = self.maze.cell_at(
                ghost.pos.x, ghost.pos.y, self.maze_area)
            if gcell != cell:
                continue
            if ghost.frightened:
                self.score += self.config.points_per_ghost
                sfx.play("pacman_eatghost.wav")
                ghost.eaten(self.maze_area)
            else:
                self.lose_life()
                break

    def lose_life(self) -> None:
        """Retire une vie ; respawn si encore des vies, sinon game over."""
        sfx.play("pacman_death.wav")
        self.lives -= 1
        if self.lives <= 0:
            from src.scenes.gameover import GameOver
            self.next_scene = GameOver(
                self.fonts, self.screen_rect, self.config, self.score)
            return
        self.respawn()

    def respawn(self) -> None:
        """Replace pacman au centre et les ghosts à leur coin."""
        sx, sy = self.maze.find_open_cell(self.maze_area)
        self.pacman.pos = pygame.Vector2(sx, sy)
        self.pacman.vel = pygame.Vector2(0, 0)
        self.pacman.queued_dir = None
        for ghost in self.ghosts:
            ghost.reset(self.maze_area)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.pacman.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        self.maze.draw(screen, self.maze_area)
        self.gum.draw(screen, self.maze_area, self.maze)
        for ghost in self.ghosts:
            ghost.draw(screen, self.maze_area)
        self.hud.draw(screen, self.hud_area,
                      self.score, self.lives, self.time_left)

        pac_rect = self.pacman.pac.get_rect(center=(int(self.pacman.pos.x),
                                                    int(self.pacman.pos.y)))
        screen.blit(self.pacman.pac, pac_rect)
