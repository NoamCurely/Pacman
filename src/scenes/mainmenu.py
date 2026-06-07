import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu


class MainMenu(Menu):
    """Menu principal: navigation flèches, validation Entrée."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, cheat: bool = False,
                 selected: int = 0) -> None:
        super().__init__(fonts, screen_rect, config)
        self.selected = selected
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
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
        _, action = self.options[self.selected]
        if action is not None:
            action()

    def start(self) -> None:
        from src.scenes.game import Game
        self.next_scene = Game(self.fonts, self.screen_rect, self.config)

    def highscores(self) -> None:
        from src.scenes.highscores import Highscores
        self.next_scene = Highscores(
            self.fonts,
            self.screen_rect,
            self.config,
            self)

    def instructions(self) -> None:
        from src.scenes.instructions import Instructions
        self.next_scene = Instructions(
            self.fonts,
            self.screen_rect,
            self.config,
            self
        )

    def toggle_cheat(self) -> None:
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
        from src.scenes.custom import Custom
        self.next_scene = Custom(
            self.fonts, self.screen_rect, self.config, self)

    def exit(self) -> None:
        self.should_quit = True
