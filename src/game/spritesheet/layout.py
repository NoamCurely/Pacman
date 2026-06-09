"""Sprite coordinates on the Pac-Man arcade sheet (pixels)."""
from pathlib import Path

ASSET_DIR = Path(__file__).parent.parent.parent.parent / "assets"
SHEET_NAME = "Arcade - Pac-Man - Miscellaneous - General Sprites.png"

TILE = 16

GHOST_X0 = 4
GHOST_ROWS = {"blinky": 64, "pinky": 80, "inky": 96, "clyde": 112}
GHOST_DIRS = ("right", "down", "left", "up")

PACMAN_OPEN_X = (4, 20)
PACMAN_CLOSED_RECT = (36, 0, TILE, TILE)
PACMAN_ROWS = {"right": 0, "left": 16, "up": 32, "down": 48}

PACGUM_RECT = (164, 177, 16, 16)
SUPERGUM_RECT = (164, 193, 16, 16)

FRIGHT_Y = 64
FRIGHT_BLUE_X = (132, 148)
FRIGHT_WHITE_X = (164, 180)

DEATH_Y = 0
DEATH_X = (52, 68, 84, 100, 116, 132, 148, 164, 180, 196, 212)
