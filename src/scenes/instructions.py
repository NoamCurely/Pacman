import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene


class Instructions(Menu):
    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, previous: Scene) -> None:
        super().__init__(fonts, screen_rect, config)
        self.previous = previous
        self.start_y = 100

        self.lines = ['HELP']

        with open('src/scenes/help.md', 'r') as f:
            self.lines = self.lines + f.readlines()

        self.keymap[pygame.K_UP] = self.restrict
        self.keymap[pygame.K_DOWN] = self.restrict
        self.keymap[pygame.K_ESCAPE] = self.back

    def draw(self, screen: pygame.Surface) -> None:
        line_height = self.font.get_linesize()
        screen.fill('black')
        txt_color = 'GREY'
        for i, line in enumerate(self.lines):
            if (line == 'HELP'):
                txt_color = 'WHITE'

            surf = self.font.render(line.strip(), True, txt_color)
            rect = surf.get_rect(center=(self.screen_rect.centerx,
                                         self.start_y + i * line_height))
            screen.blit(surf, rect)
            txt_color = 'GREY'

    def back(self) -> None:
        self.next_scene = self.previous
