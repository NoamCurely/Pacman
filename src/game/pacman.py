import pygame

from src.game.controller import Controller
from src.game.spritesheet import SpriteSheet, load_death


class Pacman(Controller):

    def __init__(self, screen_rect: pygame.Rect) -> None:
        super().__init__(screen_rect)
        self.death_frames = [
            SpriteSheet.scale(f, 32) for f in load_death(self.sheet)]
