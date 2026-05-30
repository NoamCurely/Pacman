import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene
from src.game.maze import Maze


class Game(Scene):
    """Scène de jeu: affiche le labyrinthe du niveau courant."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        level = config.levels[0]
        self.maze = Maze(level.width, level.height, seed=config.seed)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        self.maze.draw(screen)
