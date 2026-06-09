import pygame
from src.fonts import Fonts
from src.game.spritesheet import load_pacman_dir, SpriteSheet

TEXT_COLOR = (240, 240, 240)
CHEAT_COLOR = (255, 220, 0)
ACTIVE_COLOR = (100, 255, 100)
OFF_COLOR = (120, 120, 120)
TITLE = (255, 255, 255)


class Hud:

    def __init__(
        self,
        fonts: Fonts,
        area: pygame.Rect,
        cheats: dict[str, bool] | None = None
    ) -> None:
        self.fonts = fonts
        self.cheats = cheats or {}
        self.sheet = SpriteSheet()
        size = max(12, round(area.height * 0.5))
        self.font = fonts.get("Pacmania.otf", size)
        self.cheat_font = fonts.get("Pacmania.otf", 24)
        self.title = fonts.get("Pacmania.otf", 32)
        self.pac = load_pacman_dir(self.sheet, "right")[2]
        self.pac = SpriteSheet.scale(self.pac, 32)

    def draw_cheat(
        self,
        screen: pygame.Surface,
        panel: pygame.Rect,
        cheats: dict[str, bool]
    ) -> None:
        if not cheats:
            return

        title = self.title.render("CHEATS", True, TITLE)
        screen.blit(title, title.get_rect(centerx=panel.centerx - 260,
                                          top=panel.top + 10))

        labels = {
            'invincible': 'I  - Invincible',
            'noclip': 'N  - Noclip',
            'frighten': 'F  - Frighten All Ghosts',
            'end': 'G  - End Game',
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
        labels = [
            f"Score: {score}",
            "Lives:",
            f"Time: {time_left}",
            f"Level: {level}"
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
