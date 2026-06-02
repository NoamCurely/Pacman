import pygame
from pathlib import Path

ASSET_DIR = Path(__file__).parent.parent.parent / "assets"
SHEET_NAME = "Arcade - Pac-Man - Miscellaneous - General Sprites.png"

# Grille de la feuille: pas de 16px, contenu utile ~14px (origine +1).
# On extrait des tuiles de 16x16 et on laisse le padding transparent.
TILE = 16


class SpriteSheet:
    """Charge la feuille une fois, extrait les sprites à la volée.

    Pas de découpe sur disque: une vue (subsurface) par sprite, copiée
    pour rester indépendante de la feuille source.
    """

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


# --- Table de coordonnées ------------------------------------------------
# x d'origine des tuiles ghost/pacman = 4 (tuile 16 englobant le contenu).
# Lignes de fantômes: pitch 16px régulier.
GHOST_X0 = 4
GHOST_ROWS = {
    "blinky": 64,   # rouge
    "pinky": 80,    # rose
    "inky": 96,     # cyan
    "clyde": 112,   # orange
}

# 8 premières tuiles d'une ligne fantôme = 2 frames x 4 directions.
# Ordre observé sur la feuille: right, down, left, up (2 frames chacun).
GHOST_DIRS = ("right", "down", "left", "up")


def load_ghost(sheet: SpriteSheet, color: str) -> dict[str, list]:
    """Frames d'un fantôme par direction: {dir: [frame0, frame1]}."""
    y = GHOST_ROWS[color]
    frames = sheet.row(GHOST_X0, y, 8)
    out: dict[str, list] = {}
    for i, d in enumerate(GHOST_DIRS):
        out[d] = [frames[i * 2], frames[i * 2 + 1]]
    return out


# Petit Pac-Man: 2 frames (bouche) sur la bande y=48, origine x=4, pitch 16.
PACMAN_X0 = 4
PACMAN_Y = 48


def load_pacman(sheet: SpriteSheet) -> list[pygame.Surface]:
    """Frames du petit Pac-Man (bouche ouverte/fermée)."""
    return sheet.row(PACMAN_X0, PACMAN_Y, 2)


# Pastilles, blobs #FFB7AE. Tuiles 16px centrées sur le contenu.
PACGUM_RECT = (164, 177, 16, 16)     # dot 4x4 centré ~(170,181)
SUPERGUM_RECT = (164, 193, 16, 16)   # blob 8x8 centré ~(168,197)


def load_pacgum(sheet: SpriteSheet) -> pygame.Surface:
    """Pastille normale."""
    return sheet.at(*PACGUM_RECT)


def load_supergum(sheet: SpriteSheet) -> pygame.Surface:
    """Super pastille (power pellet)."""
    return sheet.at(*SUPERGUM_RECT)
