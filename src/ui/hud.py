import pygame
from src.fonts import Fonts

# Couleur du texte HUD (clair sur fond sombre).
TEXT_COLOR = (240, 240, 240)


class Hud:
    """Bandeau d'infos: score, vies, temps. Composant de dessin pur.

    La scène fournit les valeurs et le Rect cible; le HUD se contente
    de les afficher, sans connaître la logique de jeu.
    """

    def __init__(self, fonts: Fonts, area: pygame.Rect) -> None:
        self.fonts = fonts
        # police dimensionnée par la hauteur de la bande
        size = max(12, round(area.height * 0.5))
        self.font = fonts.get("Pacmania.otf", size)

    def draw(self, screen: pygame.Surface, area: pygame.Rect,
             score: int, lives: int, time_left: int) -> None:
        labels = [
            f"Score: {score}",
            f"lives: {lives}",
            f"Time: {time_left}",
        ]
        # trois colonnes réparties sur la largeur
        n = len(labels)
        for i, text in enumerate(labels):
            surf = self.font.render(text, True, TEXT_COLOR)
            cx = area.x + area.width * (2 * i + 1) // (2 * n)
            rect = surf.get_rect(center=(cx, area.centery))
            screen.blit(surf, rect)
