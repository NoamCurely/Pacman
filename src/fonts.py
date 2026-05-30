import pygame
from pathlib import Path

FONT_DIR = Path(__file__).parent.parent / "fonts"


class Fonts:
    def __init__(self) -> None:
        self.cache: dict[tuple[str, int], pygame.font.Font] = {}

    def get(self, name: str, size: int) -> pygame.font.Font:
        key = (name, size)
        if key not in self.cache:
            try:
                self.cache[key] = pygame.font.Font(FONT_DIR / name, size)
            except FileNotFoundError:
                print(f"Warning: font {name} missing, using default")
                self.cache[key] = pygame.font.Font(None, size)
        return self.cache[key]