"""NameEntry: prompt the player for a name to save the score."""
import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene, scaled
from src.ui.confirm import ConfirmDialog


class NameEntry(Scene):
    """Name input modal; ENTER saves the score then returns to the menu."""

    MAX_LEN = 12

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
        self.name = ""
        h = screen_rect.height
        title_font = fonts.get("Pacmania.otf", scaled(h, 64))
        hint_font = fonts.get("Pacmania.otf", scaled(h, 32))
        self.dialog = ConfirmDialog(
            title_font, hint_font, gap=scaled(h, 90))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Edit the name from key presses; confirm on ENTER."""
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_RETURN:
            if self.name:
                self.confirm()
        elif event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.unicode.isprintable() and event.unicode != "":
            if len(self.name) < self.MAX_LEN:
                self.name += event.unicode

    def confirm(self) -> None:
        """Save the score under the entered name and return to the menu."""
        from src.scenes.highscores import Highscores
        from src.scenes.mainmenu import MainMenu
        menu = MainMenu(self.fonts, self.screen_rect, self.config)
        hs = Highscores(self.fonts, self.screen_rect, self.config, menu)
        hs.add_score(self.name, self.score)
        self.next_scene = menu

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the modal with the name and a blinking cursor."""
        screen.fill("black")
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        self.dialog.draw(screen, self.screen_rect,
                         "ENTER NAME", self.name + cursor)
