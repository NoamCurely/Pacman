import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene
from src.ui.confirm import ConfirmDialog


class NameEntry(Scene):
    """Modal de saisie du pseudo. ENTER -> sauve le score puis menu."""

    MAX_LEN = 12

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, score: int) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        self.score = score
        self.name = ""
        h = screen_rect.height
        title_font = fonts.get("Pacmania.otf", round(h * 64 / 720))
        hint_font = fonts.get("Pacmania.otf", round(h * 32 / 720))
        self.dialog = ConfirmDialog(
            title_font, hint_font, gap=round(h * 90 / 720))

    def handle_event(self, event: pygame.event.Event) -> None:
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
        from src.scenes.highscores import Highscores
        from src.scenes.mainmenu import MainMenu
        menu = MainMenu(self.fonts, self.screen_rect, self.config)
        hs = Highscores(self.fonts, self.screen_rect, self.config, menu)
        hs.add_score(self.name, self.score)
        self.next_scene = menu

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        # curseur clignotant
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        self.dialog.draw(screen, self.screen_rect,
                         "ENTER NAME", self.name + cursor)
