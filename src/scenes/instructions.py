"""Instructions: scrollable help text loaded from help.md."""
from pathlib import Path

import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene, scaled

HELP_PATH = Path(__file__).parent / "help.md"


class Instructions(Menu):
    """Display the controls and rules read from help.md."""

    def __init__(
        self, 
        fonts: Fonts, 
        screen_rect: pygame.Rect,
        config: Config, 
        previous: Scene
    ) -> None:
        super().__init__(fonts, screen_rect, config)
        self.previous = previous
        self.start_y = scaled(screen_rect.height, 50)
        self.help_font = fonts.get("Pacmania.otf", scaled(screen_rect.height, 28))
        self.lines  = []

        try:
            with open(HELP_PATH, 'r') as f:
                self.lines = self.lines + f.readlines()
        except FileNotFoundError:
            print(f"Warning: {HELP_PATH} missing")

        self.keymap[pygame.K_UP] = self.restrict
        self.keymap[pygame.K_DOWN] = self.restrict
        self.keymap[pygame.K_ESCAPE] = self.back

    def draw(self, screen: pygame.Surface) -> None:
        """Draw each help line, highlighting the header."""
        txt_color = 'WHITE'
        line_height = self.font.get_linesize()
        screen.fill('black')
        for i, line in enumerate(self.lines):
            surf = self.help_font.render(line.strip(), True, txt_color)
            rect = surf.get_rect(center=(self.screen_rect.centerx,
                                         self.start_y + i * line_height))
            screen.blit(surf, rect)

    def back(self) -> None:
        """Return to the previous scene."""
        self.next_scene = self.previous
