"""Sounds: cache and play sound effects, tolerant of a missing mixer."""
from __future__ import annotations

from pathlib import Path

import pygame

SOUND_DIR = Path(__file__).parent.parent / "sound"


class Sounds:
    """Lazily load and play cached sound effects."""

    def __init__(self) -> None:
        self.cache: dict[str, pygame.mixer.Sound] = {}
        self.muted = False

    def get(self, name: str) -> pygame.mixer.Sound | None:
        """Return the cached sound, or None if it cannot be loaded."""
        if name not in self.cache:
            try:
                self.cache[name] = pygame.mixer.Sound(
                    str(SOUND_DIR / name))
            except (FileNotFoundError, pygame.error, NotImplementedError):
                print(f"Warning: sound {name} missing or audio unavailable")
                return None
        return self.cache[name]

    def play(self, name: str) -> None:
        """Play the named sound unless muted."""
        if self.muted:
            return
        snd = self.get(name)
        if snd is not None:
            snd.play()


sfx = Sounds()
