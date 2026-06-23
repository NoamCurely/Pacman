"""HUD: score, lives, time, level and the cheat panel overlay."""
import pygame

from src.fonts import Fonts
from src.game.spritesheet import load_pacman_dir, SpriteSheet

TEXT_COLOR = (240, 240, 240)
CHEAT_COLOR = (255, 220, 0)
ACTIVE_COLOR = (100, 255, 100)
OFF_COLOR = (120, 120, 120)
TITLE = (255, 255, 255)


class Hud:
    """Render the in-game HUD and the optional cheat panel."""

    def __init__(self, fonts: Fonts, area: pygame.Rect) -> None:
        self.fonts = fonts
        self.sheet = SpriteSheet()
        size = max(12, round(area.height * 0.5))
        self.font = fonts.get("Pacmania.otf", size)
        self.cheat_font = fonts.get("Pacmania.otf", 24)
        self.title = fonts.get("Pacmania.otf", 32)
        self.pac = load_pacman_dir(self.sheet, "right")[1]
        self.pac = SpriteSheet.scale(self.pac, 32)

    def draw_cheat(
        self,
        screen: pygame.Surface,
        panel: pygame.Rect,
        cheats: dict[str, bool]
    ) -> None:
        """Draw the cheat panel listing each toggle and its state."""
        if not cheats:
            return

        title = self.title.render("CHEATS", True, TITLE)
        screen.blit(title, title.get_rect(centerx=panel.centerx - 260,
                                          top=panel.top + 10))

        labels = {
            'invincible': 'I  - Invincible',
            'noclip': 'N  - Noclip',
            'frozen': 'R    - Freeze All Ghosts',
            'frighten': 'F  - Frighten All Ghosts',
            'end': 'G  - Skip Level',
            'add_life': 'L - Extra Life',
            'o': 'O - Reduce Speed',
            'p': 'P - Increase Speed'
        }

        y = panel.top + 40
        for key, label in labels.items():
            active = cheats.get(key, False)
            color = ACTIVE_COLOR if active else OFF_COLOR
            surf = self.cheat_font.render(label, True, color)
            screen.blit(surf, surf.get_rect(left=panel.left - 260, top=y + 5))
            y += self.cheat_font.get_linesize() + 4

    def draw(
        self,
        screen: pygame.Surface,
        area: pygame.Rect,
        score: int,
        lives: int,
        time_left: int,
        level: int
    ) -> None:
        """Draw score, lives, time and level across the HUD bar."""
        labels = [
            f"Score: {score}",
            "Lives:",
            f"Time: {time_left}",
            f"Level: {level}"
        ]
        n = len(labels)
        rects = []
        plus = 0
        if (lives >= 8):
            plus = lives - 8
        for i, text in enumerate(labels):
            surf = self.font.render(text, True, TEXT_COLOR)
            cx = area.x + area.width * (2 * i + 1) // (2 * n)
            rect = surf.get_rect(center=(cx, area.centery))
            screen.blit(surf, rect)
            rects.append(rect)
        lives_rect = rects[1]
        lives_display = lives if lives <= 8 else 8
        gap = 19
        for _ in range(lives_display):
            pac_rect = self.pac.get_rect(midright=(
                gap + lives_rect.right + gap, area.centery + 4))
            screen.blit(self.pac, pac_rect)
            gap += 17
        if (plus):
            plus_display = self.font.render(f"+{plus}", True, TEXT_COLOR)
            rect = plus_display.get_rect(center=(1090, area.centery))
            screen.blit(plus_display, rect)
