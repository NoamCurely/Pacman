from collections.abc import Callable

import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene


class Menu(Scene):

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        h = screen_rect.height
        self.font = fonts.get("Pacmania.otf", round(h * 48 / 720))
        self.selected = 0
        self.options: list[tuple[str, Callable[[], None] | None]] = []
        self.start_y = round(h * 200 / 720)
        self.step = round(h * 80 / 720)
        self.keymap = {
            pygame.K_DOWN: lambda: self.move(1),
            pygame.K_UP: lambda: self.move(-1),
        }

    def move(self, d: int) -> None:
        self.selected = (self.selected + d) % len(self.options)

    def labels(self) -> list[str]:
        return [label for label, _ in self.options]

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        for i, label in enumerate(self.labels()):
            color: str | tuple[int, int, int]
            if i == self.selected:
                color = "yellow"
            else:
                color = (120, 120, 120)
            surf = self.font.render(label, True, color)
            rect = surf.get_rect(
                center=(self.screen_rect.centerx,
                        self.start_y + i * self.step))
            screen.blit(surf, rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        action = self.keymap.get(event.key)
        if action:
            action()

    @staticmethod
    def restrict() -> None:
        pass
