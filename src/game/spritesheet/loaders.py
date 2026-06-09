"""Build game-specific sprite sets from a SpriteSheet and the layout."""
import pygame

from . import layout
from .sheet import SpriteSheet

__all__ = [
    "load_ghost",
    "load_pacman",
    "load_pacman_dir",
    "load_pacman_closed",
    "load_pacgum",
    "load_supergum",
    "load_frightened",
    "load_death",
]

Frames = dict[str, list[pygame.Surface]]


def load_ghost(sheet: SpriteSheet, color: str) -> Frames:
    """Return the ghost frames keyed by direction for one color."""
    frames = sheet.row(layout.GHOST_X0, layout.GHOST_ROWS[color], 8)
    return {
        d: [frames[i * 2], frames[i * 2 + 1]]
        for i, d in enumerate(layout.GHOST_DIRS)
    }


def load_pacman_closed(sheet: SpriteSheet) -> pygame.Surface:
    """Return the closed-mouth Pac-Man sprite."""
    return sheet.at(*layout.PACMAN_CLOSED_RECT)


def load_pacman_dir(
    sheet: SpriteSheet,
    direction: str,
) -> list[pygame.Surface]:
    """Return the Pac-Man animation frames for one direction."""
    y = layout.PACMAN_ROWS[direction]
    closed = load_pacman_closed(sheet)
    half = sheet.at(layout.PACMAN_OPEN_X[1], y)
    wide = sheet.at(layout.PACMAN_OPEN_X[0], y)
    return [closed, half, wide]


def load_pacman(sheet: SpriteSheet) -> Frames:
    """Return Pac-Man frames keyed by direction."""
    return {d: load_pacman_dir(sheet, d) for d in layout.PACMAN_ROWS}


def load_pacgum(sheet: SpriteSheet) -> pygame.Surface:
    """Return the pacgum (dot) sprite."""
    return sheet.at(*layout.PACGUM_RECT)


def load_supergum(sheet: SpriteSheet) -> pygame.Surface:
    """Return the super-pacgum (power pellet) sprite."""
    return sheet.at(*layout.SUPERGUM_RECT)


def load_frightened(sheet: SpriteSheet) -> Frames:
    """Return frightened frames keyed by 'blue' and 'white'."""
    blue = [sheet.at(x, layout.FRIGHT_Y) for x in layout.FRIGHT_BLUE_X]
    white = [sheet.at(x, layout.FRIGHT_Y) for x in layout.FRIGHT_WHITE_X]
    return {"blue": blue, "white": white}


def load_death(sheet: SpriteSheet) -> list[pygame.Surface]:
    """Return the Pac-Man death animation frames."""
    return [sheet.at(x, layout.DEATH_Y) for x in layout.DEATH_X]
