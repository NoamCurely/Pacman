import pygame
from pathlib import Path

ASSET_DIR = Path(__file__).parent.parent.parent / "assets"
SHEET_NAME = "Arcade - Pac-Man - Miscellaneous - General Sprites.png"

TILE = 16


class SpriteSheet:
   

    def __init__(self, path: str | Path | None = None) -> None:
        if path is None:
            path = ASSET_DIR / SHEET_NAME
        self.sheet = pygame.image.load(str(path)).convert_alpha()

    def at(self, x: int, y: int,
           w: int = TILE, h: int = TILE) -> pygame.Surface:
        """Un sprite au rect (x, y, w, h)."""
        return self.sheet.subsurface(pygame.Rect(x, y, w, h)).copy()

    def row(self, x0: int, y: int, n: int,
            pitch: int = TILE, size: int = TILE) -> list[pygame.Surface]:
        """n sprites alignés horizontalement depuis (x0, y)."""
        return [self.at(x0 + i * pitch, y, size, size) for i in range(n)]

    @staticmethod
    def scale(spr: pygame.Surface, size: int) -> pygame.Surface:
        """Met un sprite à l'échelle (carré), sans lissage (pixel art)."""
        return pygame.transform.scale(spr, (size, size))



GHOST_X0 = 4
GHOST_ROWS = {
    "blinky": 64,   # rouge
    "pinky": 80,    # rose
    "inky": 96,     # cyan
    "clyde": 112,   # orange
}


GHOST_DIRS = ("right", "down", "left", "up")


def load_ghost(sheet: SpriteSheet,
               color: str) -> dict[str, list[pygame.Surface]]:
    """Frames d'un fantôme par direction: {dir: [frame0, frame1]}."""
    y = GHOST_ROWS[color]
    frames = sheet.row(GHOST_X0, y, 8)
    out: dict[str, list[pygame.Surface]] = {}
    for i, d in enumerate(GHOST_DIRS):
        out[d] = [frames[i * 2], frames[i * 2 + 1]]
    return out



PACMAN_X0 = 4
PACMAN_OPEN_X = (4, 20)        # (grande ouverte, mi-ouverte)
PACMAN_CLOSED_RECT = (36, 0, TILE, TILE)  # cercle plein partagé

PACMAN_ROWS = {
    "right": 0,
    "left": 16,
    "up": 32,
    "down": 48,
}


def load_pacman_closed(sheet: SpriteSheet) -> pygame.Surface:
    return sheet.at(*PACMAN_CLOSED_RECT)


def load_pacman_dir(sheet: SpriteSheet,
                    direction: str) -> list[pygame.Surface]:
    y = PACMAN_ROWS[direction]
    closed = load_pacman_closed(sheet)
    half = sheet.at(PACMAN_OPEN_X[1], y)
    wide = sheet.at(PACMAN_OPEN_X[0], y)
    return [closed, half, wide]


def load_pacman(sheet: SpriteSheet) -> dict[str, list[pygame.Surface]]:
    """Toutes les directions: {dir: [fermé, mi, grand]}."""
    return {d: load_pacman_dir(sheet, d) for d in PACMAN_ROWS}


# Pastilles, blobs #FFB7AE. Tuiles 16px centrées sur le contenu.
PACGUM_RECT = (164, 177, 16, 16)     # dot 4x4 centré ~(170,181)
SUPERGUM_RECT = (164, 193, 16, 16)   # blob 8x8 centré ~(168,197)


def load_pacgum(sheet: SpriteSheet) -> pygame.Surface:
    """Pastille normale."""
    return sheet.at(*PACGUM_RECT)


def load_supergum(sheet: SpriteSheet) -> pygame.Surface:
    """Super pastille (power pellet)."""
    return sheet.at(*SUPERGUM_RECT)


# Frightened: ligne du red (y=64), après les 8 tuiles directionnelles.
FRIGHT_Y = 64
FRIGHT_BLUE_X = (132, 148)    # 2 frames bleues
FRIGHT_WHITE_X = (164, 180)   # 2 frames blanches (clignotement de fin)


def load_frightened(sheet: SpriteSheet) -> dict[str, list[pygame.Surface]]:
    """Frames frightened : {'blue': [..], 'white': [..]}."""
    blue = [sheet.at(x, FRIGHT_Y) for x in FRIGHT_BLUE_X]
    white = [sheet.at(x, FRIGHT_Y) for x in FRIGHT_WHITE_X]
    return {"blue": blue, "white": white}


# Animation de mort (ligne du haut, y=0) : pacman s'ouvre puis disparaît.
DEATH_Y = 0
DEATH_X = (52, 68, 84, 100, 116, 132, 148, 164, 180, 196, 212)


def load_death(sheet: SpriteSheet) -> list[pygame.Surface]:
    """Les 11 frames de l'animation de mort."""
    return [sheet.at(x, DEATH_Y) for x in DEATH_X]
