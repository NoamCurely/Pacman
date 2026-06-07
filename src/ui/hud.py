import pygame
from src.fonts import Fonts
from src.game.spritesheet import load_pacman_dir, SpriteSheet


# Couleur du texte HUD (clair sur fond sombre).
TEXT_COLOR = (240, 240, 240)


class Hud:
    """Bandeau d'infos: score, vies, temps. Composant de dessin pur.

    La scène fournit les valeurs et le Rect cible; le HUD se contente
    de les afficher, sans connaître la logique de jeu.
    """

    def __init__(self, fonts: Fonts, area: pygame.Rect) -> None:
        self.fonts = fonts
        self.sheet = SpriteSheet()
        size = max(12, round(area.height * 0.5))
        self.font = fonts.get("Pacmania.otf", size)
        self.pac = load_pacman_dir(self.sheet, "right")[2]
        self.pac = SpriteSheet.scale(self.pac, 32)

    def draw(self, screen: pygame.Surface, area: pygame.Rect,
             score: int, lives: int, time_left: int) -> None:
        labels = [
            f"Score: {score}",
            "Lives:",
            f"Time: {time_left}",
        ]
        n = len(labels)
        rects = []
        for i, text in enumerate(labels):
            surf = self.font.render(text, True, TEXT_COLOR)
            cx = area.x + area.width * (2 * i + 1) // (2 * n)
            rect = surf.get_rect(center=(cx, area.centery))
            screen.blit(surf, rect)
            rects.append(rect)
        lives_rect = rects[1]
        gap = 18
        for _ in range(lives):
            pac_rect = self.pac.get_rect(midright=(
                gap + lives_rect.right + gap, area.centery + 2))
            screen.blit(self.pac, pac_rect)
            gap += 20
