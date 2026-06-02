import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene


class Landing(Scene):
    """Écran titre: 'PAC-MAN' + invite clignotante. Entrée -> menu."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config

        h = screen_rect.height
        title_font = fonts.get("Pacmania.otf", round(h * 74 / 720))
        prompt_font = fonts.get("Pacmania.otf", round(h * 32 / 720))

        self.title = title_font.render("PAC-MAN", True, "yellow")
        self.title_rect = self.title.get_rect(center=screen_rect.center)

        self.prompt = prompt_font.render(
            "PRESS ENTER TO START", True, (200, 200, 200))
        self.prompt_rect = self.prompt.get_rect(
            center=(screen_rect.centerx,
                    screen_rect.centery + round(h * 100 / 720)))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from src.scenes.mainmenu import MainMenu
            self.next_scene = MainMenu(
                self.fonts, self.screen_rect, self.config)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        screen.blit(self.title, self.title_rect)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            screen.blit(self.prompt, self.prompt_rect)
