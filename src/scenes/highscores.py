import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene
from json import loads, dump


class Highscores(Menu):
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
        self.font = fonts.get("Pacmania.otf", round(h * 32 / 720))
        self.title = fonts.get("Pacmania.otf", round(h * 64 / 720))
        self.start_y = round(h * 100 / 720)

        with open('src/saves/highscores.json', 'r') as f:
            self.data = loads(f.read())

        self.keymap[pygame.K_UP] = self.restrict
        self.keymap[pygame.K_DOWN] = self.restrict
        self.keymap[pygame.K_ESCAPE] = self.back

    def draw(self, screen: pygame.Surface) -> None:
        line_height = self.font.get_linesize()
        screen.fill('black')
        txt_color = 'GREY'

        sorted_data = sorted(
            self.data, key=lambda x: x['score'], reverse=True
        )

        t_surf = self.title.render("HIGHSCORES", True, "YELLOW")
        t_rect = t_surf.get_rect(
            center=(self.screen_rect.centerx,
                    self.start_y - round(self.screen_rect.height * 50 / 720)))
        screen.blit(t_surf, t_rect)

        list_top = self.start_y + round(self.screen_rect.height * 60 / 720)
        for i, entry in enumerate(sorted_data):
            surf = self.font.render(
                entry['name'] + '   -   ' + str(entry['score']),
                True,
                txt_color)
            rect = surf.get_rect(center=(self.screen_rect.centerx,
                                         list_top + i * line_height))
            screen.blit(surf, rect)

    def add_score(self, name: str, score: int) -> None:
        if self.if_exist(name):
            self.update_score(name, score)
            return

        self.data.append({'name': name, 'score': score})
        dump(self.data, open('src/saves/highscores.json', 'w'), indent=2)

    def update_score(self, name: str, score: int) -> None:
        for entry in self.data:
            if entry['name'] == name:
                entry['score'] = score
                break

        dump(self.data, open('src/saves/highscores.json', 'w'), indent=2)

    def if_exist(self, name: str) -> bool:
        for entry in self.data:
            if entry['name'] == name:
                return True
        return False

    def back(self) -> None:
        self.next_scene = self.previous
