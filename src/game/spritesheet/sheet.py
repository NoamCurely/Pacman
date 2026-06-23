"""Generic sprite-sheet reader: grab sub-surfaces from a single image."""
from pathlib import Path

import pygame

from .layout import ASSET_DIR, SHEET_NAME, TILE


class SpriteSheet:
    """Load an image once and slice tiles out of it."""

    def __init__(self, path: str | Path | None = None) -> None:
        if path is None:
            path = ASSET_DIR / SHEET_NAME
        # The arcade sheet has a solid black background (no real alpha), so
        # convert() + a black colorkey makes it transparent. convert_alpha()
        # would give per-pixel alpha, which makes blit ignore the colorkey.
        self.sheet = pygame.image.load(str(path)).convert()
        self.sheet.set_colorkey((0, 0, 0))

    def at(
        self,
        x: int,
        y: int,
        w: int = TILE,
        h: int = TILE,
    ) -> pygame.Surface:
        """Return a copy of the sub-surface at the given rect."""
        return self.sheet.subsurface(pygame.Rect(x, y, w, h)).copy()

    def row(
        self,
        x0: int,
        y: int,
        n: int,
        pitch: int = TILE,
        size: int = TILE,
    ) -> list[pygame.Surface]:
        """Return n tiles laid out horizontally from x0 at row y."""
        return [self.at(x0 + i * pitch, y, size, size) for i in range(n)]

    @staticmethod
    def scale(spr: pygame.Surface, size: int) -> pygame.Surface:
        """Return spr scaled to a square of the given size."""
        return pygame.transform.scale(spr, (size, size))
