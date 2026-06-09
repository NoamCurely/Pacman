import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene
from src.ui.confirm import ConfirmDialog


class GameOver(Scene):
    """Modal 'GAME OVER' + score. ENTER -> saisie pseudo, cooldown -> menu."""

    COOLDOWN_MS = 30000

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, score: int) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        self.score = score
        h = screen_rect.height
        title_font = fonts.get("Pacmania.otf", round(h * 64 / 720))
        hint_font = fonts.get("Pacmania.otf", round(h * 32 / 720))
        self.dialog = ConfirmDialog(title_font, hint_font)
        self.start = pygame.time.get_ticks()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from src.scenes.nameentry import NameEntry
            self.next_scene = NameEntry(
                self.fonts, self.screen_rect, self.config, self.score)

    def update(self) -> None:
        if pygame.time.get_ticks() - self.start >= self.COOLDOWN_MS:
            self.to_menu()

    def to_menu(self) -> None:
        from src.scenes.mainmenu import MainMenu
        self.next_scene = MainMenu(
            self.fonts, self.screen_rect, self.config)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        self.dialog.draw(screen, self.screen_rect,
                         "GAME OVER", f"SCORE: {self.score}")
