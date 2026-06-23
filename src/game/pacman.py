import pygame

from src.game.controller import Controller
from src.game.spritesheet import SpriteSheet, load_death


class Pacman(Controller):

    def __init__(self, screen_rect: pygame.Rect) -> None:
        self._raw_death: list[pygame.Surface] | None = None
        self.death_frames: list[pygame.Surface] = []
        super().__init__(screen_rect)

    def resize(self, size: int) -> None:
        """Rescale movement and death sprites to one maze cell."""
        super().resize(size)
        if self._raw_death is None:
            self._raw_death = load_death(self.sheet)
        self.death_frames = [
            SpriteSheet.scale(f, size) for f in self._raw_death]
