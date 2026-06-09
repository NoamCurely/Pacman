"""Victory: end screen shown when every level is cleared."""
import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene, scaled


class Victory(Scene):
    """Victory screen; ENTER goes to the name entry."""

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
        self.title_font = fonts.get("Pacmania.otf", scaled(h, 64))
        self.font = fonts.get("Pacmania.otf", scaled(h, 32))
        self.small_font = fonts.get("Pacmania.otf", scaled(h, 24))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Go to the name entry when ENTER is pressed."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from src.scenes.nameentry import NameEntry
            self.next_scene = NameEntry(
                self.fonts, self.screen_rect, self.config, self.score)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the win message, the score and the continue hint."""
        screen.fill((0, 0, 0))
        cx = self.screen_rect.centerx
        cy = self.screen_rect.centery
        h = self.screen_rect.height

        t = self.title_font.render("YOU WIN!", True, self.WIN_COLOR)
        screen.blit(t, t.get_rect(center=(cx, cy - scaled(h, 120))))

        s = self.font.render(f"Score: {self.score}", True, self.TEXT_COLOR)
        screen.blit(s, s.get_rect(center=(cx, cy - scaled(h, 40))))

        hint = self.small_font.render(
            "Press ENTER to continue", True, self.DIM_COLOR)
        screen.blit(hint, hint.get_rect(center=(cx, cy + scaled(h, 60))))
