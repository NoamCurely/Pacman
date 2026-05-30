import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu


class MainMenu(Menu):
    """Menu principal: navigation flèches, validation Entrée."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config) -> None:
        super().__init__(fonts, screen_rect, config)
        self.options = [
            ("START GAME", self.start),
            ("HIGHSCORES", self.highscores),
            ("INSTRUCTIONS", self.instructions),
            ("CHEAT", self.cheat),
            ("CUSTOM", self.custom),
            ("EXIT", self.exit),
        ]
        self.keymap[pygame.K_RETURN] = self.choose

    def choose(self) -> None:
        _, action = self.options[self.selected]
        action()

    def start(self) -> None:
        from src.scenes.game import Game
        self.next_scene = Game(self.fonts, self.screen_rect, self.config)

    def highscores(self) -> None:
        pass

    def instructions(self) -> None:
        pass

    def cheat(self) -> None:
        pass

    def custom(self) -> None:
        from src.scenes.custom import Custom
        self.next_scene = Custom(
            self.fonts, self.screen_rect, self.config, self)

    def exit(self) -> None:
        self.should_quit = True
