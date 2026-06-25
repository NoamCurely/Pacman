"""Highscores: load, display and persist the top scores."""
from json import loads, dump

import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene, scaled
from pathlib import Path


SAVE_DIR = Path('src/saves')
SAVE_PATH = SAVE_DIR / 'highscores.json'


class Highscores(Menu):
    """Menu showing the saved scores and persisting new ones."""

    def __init__(
        self,
        fonts: Fonts,
        screen_rect: pygame.Rect,
        config: Config,
        previous: Scene
    ) -> None:
        super().__init__(fonts, screen_rect, config)
        self.previous = previous
        h = screen_rect.height
        self.font = fonts.get("Pacmania.otf", scaled(h, 32))
        self.title = fonts.get("Pacmania.otf", scaled(h, 64))
        self.start_y = scaled(h, 100)

        Highscores.ensure_json()

        with open(SAVE_PATH, 'r') as f:
            self.data = loads(f.read())

        self.keymap[pygame.K_UP] = self.restrict
        self.keymap[pygame.K_DOWN] = self.restrict
        self.keymap[pygame.K_ESCAPE] = self.back

    @staticmethod
    def ensure_json() -> None:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        if not SAVE_PATH.exists():
            SAVE_PATH.write_text('[]')

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the title and the scores sorted high to low."""
        line_height = self.font.get_linesize()
        screen.fill('black')
        txt_color = 'GREY'

        sorted_data = sorted(
            self.data, key=lambda x: x['score'], reverse=True
        )

        t_surf = self.title.render("HIGHSCORES", True, "YELLOW")
        t_rect = t_surf.get_rect(
            center=(self.screen_rect.centerx,
                    self.start_y - scaled(self.screen_rect.height, 50)))
        screen.blit(t_surf, t_rect)

        list_top = self.start_y + scaled(self.screen_rect.height, 60)
        for i, entry in enumerate(sorted_data):
            surf = self.font.render(
                entry['name'] + '   -   ' + str(entry['score']),
                True,
                txt_color)
            rect = surf.get_rect(center=(self.screen_rect.centerx,
                                         list_top + i * line_height))
            screen.blit(surf, rect)

    def add_score(self, name: str, score: int) -> None:
        """Add or update the score for name and persist the list."""
        if self.if_exist(name):
            self.update_score(name, score)
            return

        self.data.append({'name': name, 'score': score})
        self.save()

    def update_score(self, name: str, score: int) -> None:
        """Overwrite an existing player's score and persist."""
        for entry in self.data:
            if entry['name'] == name:
                entry['score'] = score
                break

        self.save()

    def save(self) -> None:
        """Persist the score list to disk."""
        with open(SAVE_PATH, 'w') as f:
            dump(self.data, f, indent=2)

    def if_exist(self, name: str) -> bool:
        """Return True if a score already exists for name."""
        for entry in self.data:
            if entry['name'] == name:
                return True
        return False

    def back(self) -> None:
        """Return to the previous scene."""
        self.next_scene = self.previous
