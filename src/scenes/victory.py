import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene


class Victory(Scene):
    """Écran de victoire (tous les gums mangés). ENTER -> saisie pseudo."""

    TEXT_COLOR = (240, 240, 240)
    DIM_COLOR = (160, 160, 160)
    WIN_COLOR = (255, 220, 0)

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, score: int) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        self.score = score
        h = screen_rect.height
        self.title_font = fonts.get("Pacmania.otf", round(h * 64 / 720))
        self.font = fonts.get("Pacmania.otf", round(h * 32 / 720))
        self.small_font = fonts.get("Pacmania.otf", round(h * 24 / 720))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from src.scenes.nameentry import NameEntry
            self.next_scene = NameEntry(
                self.fonts, self.screen_rect, self.config, self.score)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        cx = self.screen_rect.centerx
        cy = self.screen_rect.centery
        h = self.screen_rect.height

        t = self.title_font.render("YOU WIN!", True, self.WIN_COLOR)
        screen.blit(t, t.get_rect(center=(cx, cy - round(h * 120 / 720))))

        s = self.font.render(f"Score: {self.score}", True, self.TEXT_COLOR)
        screen.blit(s, s.get_rect(center=(cx, cy - round(h * 40 / 720))))

        hint = self.small_font.render(
            "Press ENTER to continue", True, self.DIM_COLOR)
        screen.blit(hint, hint.get_rect(center=(cx, cy + round(h * 60 / 720))))
