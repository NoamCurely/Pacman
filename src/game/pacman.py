import pygame
from src.game.maze import Maze
from src.parsing import Config
from src.game.controller import Controller


class Pacman(Controller):
    def __init__(self, maze: Maze,
                 config: Config,
                 screen_rect: pygame.Rect) -> None:
        super().__init__(screen_rect)
