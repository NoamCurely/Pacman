"""GameOver: end screen with a cooldown back to the main menu."""
import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene, scaled
from src.ui.confirm import ConfirmDialog

COOLDOWN_MS = 30000


class GameOver(Scene):
    """Game over modal; ENTER saves a score, the cooldown returns to menu."""

    def __init__(
        self,
        fonts: Fonts,
        screen_rect: pygame.Rect,
        config: Config,
        score: int
    ) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        self.score = score
        h = screen_rect.height
        title_font = fonts.get("Pacmania.otf", scaled(h, 64))
        hint_font = fonts.get("Pacmania.otf", scaled(h, 32))
        self.dialog = ConfirmDialog(title_font, hint_font)
        self.start = pygame.time.get_ticks()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Go to the name entry when ENTER is pressed."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from src.scenes.nameentry import NameEntry
            self.next_scene = NameEntry(
                self.fonts, self.screen_rect, self.config, self.score)

    def update(self) -> None:
        """Return to the menu once the cooldown elapses."""
        if pygame.time.get_ticks() - self.start >= COOLDOWN_MS:
            self.to_menu()

    def to_menu(self) -> None:
        """Go back to the main menu."""
        from src.scenes.mainmenu import MainMenu
        self.next_scene = MainMenu(
            self.fonts, self.screen_rect, self.config)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game over modal with the final score."""
        screen.fill("black")
        self.dialog.draw(screen, self.screen_rect,
                         "GAME OVER", f"SCORE: {self.score}")
