from __future__ import annotations

import pygame
from pathlib import Path

SOUND_DIR = Path(__file__).parent.parent / "sound"


class Sounds:
    """Charge et joue les effets sonores. Cache + robuste à l'absence."""

    def __init__(self) -> None:
        self.cache: dict[str, pygame.mixer.Sound] = {}
        self.muted = False

    def get(self, name: str) -> pygame.mixer.Sound | None:
        """Charge un son (caché). None si fichier/mixer indisponible."""
        if name not in self.cache:
            try:
                self.cache[name] = pygame.mixer.Sound(
                    str(SOUND_DIR / name))
            except (FileNotFoundError, pygame.error, NotImplementedError):
                print(f"Warning: son {name} manquant ou audio indispo")
                return None
        return self.cache[name]

    def play(self, name: str) -> None:
        """Joue un effet court (rien si muet ou indisponible)."""
        if self.muted:
            return
        snd = self.get(name)
        if snd is not None:
            snd.play()



sfx = Sounds()
