"""Fonts: cache pygame fonts loaded from the fonts directory."""
from pathlib import Path

import pygame

FONT_DIR = Path(__file__).parent.parent / "fonts"


class Fonts:
    """Lazily load and cache fonts by (name, size)."""

    def __init__(self) -> None:
        self.cache: dict[tuple[str, int], pygame.font.Font] = {}

    def get(self, name: str, size: int) -> pygame.font.Font:
        """Return the cached font, loading the default on failure."""
        key = (name, size)
        if key not in self.cache:
            try:
                self.cache[key] = pygame.font.Font(FONT_DIR / name, size)
            except FileNotFoundError:
                print(f"Warning: font {name} missing, using default")
                self.cache[key] = pygame.font.Font(None, size)
        return self.cache[key]
