"""MainMenu: top-level menu wiring options to their scenes."""
import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu


class MainMenu(Menu):
    """Main menu; arrows navigate and ENTER selects."""

    def __init__(
        self, 
        fonts: Fonts, 
        screen_rect: pygame.Rect,
        config: Config, 
        cheat: bool = False,
        selected: int = 0
    ) -> None:
        super().__init__(fonts, screen_rect, config)
        self.selected = selected
        self.cheat = cheat
        self.options = [
            ("START GAME", self.start),
            ("HIGHSCORES", self.highscores),
            ("INSTRUCTIONS", self.instructions),
            ("CHEAT: " + str(self.cheat), self.toggle_cheat),
            ("CUSTOM", self.custom),
            ("EXIT", self.exit),
        ]
        self.keymap[pygame.K_RETURN] = self.choose

    def choose(self) -> None:
        """Run the action of the selected option."""
        _, action = self.options[self.selected]
        if action is not None:
            action()

    def start(self) -> None:
        """Start a new game with the current cheat setting."""
        from src.scenes.game import Game
        self.next_scene = Game(self.fonts, self.screen_rect, self.config,
                               self.cheat)

    def highscores(self) -> None:
        """Open the highscores screen."""
        from src.scenes.highscores import Highscores
        self.next_scene = Highscores(
            self.fonts,
            self.screen_rect,
            self.config,
            self)

    def instructions(self) -> None:
        """Open the instructions screen."""
        from src.scenes.instructions import Instructions
        self.next_scene = Instructions(
            self.fonts,
            self.screen_rect,
            self.config,
            self
        )

    def toggle_cheat(self) -> None:
        """Flip cheat mode and rebuild the menu labels."""
        self.cheat = not self.cheat
        MainMenu.__init__(
            self,
            self.fonts,
            self.screen_rect,
            self.config,
            self.cheat,
            self.selected
        )

    def custom(self) -> None:
        """Open the custom configuration screen."""
        from src.scenes.custom import Custom
        self.next_scene = Custom(
            self.fonts, self.screen_rect, self.config, self)

    def exit(self) -> None:
        """Request application shutdown."""
        self.should_quit = True
