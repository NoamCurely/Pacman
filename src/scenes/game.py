import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene
from src.ui.hud import Hud
from src.game.maze import Maze, BG_COLOR


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

        # découpe écran: zone maze (haut) + bande HUD (bas)
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

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        self.maze.draw(screen, self.maze_area)
        self.hud.draw(screen, self.hud_area,
                      self.score, self.lives, self.time_left)
