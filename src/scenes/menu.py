"""Menu: base vertical menu with keyboard navigation."""
from collections.abc import Callable

import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene, scaled


class Menu(Scene):
    """Selectable list of labelled options driven by arrow keys."""

    def __init__(
        self, 
        fonts: Fonts, 
        screen_rect: pygame.Rect,
        config: Config
    ) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        h = screen_rect.height
        self.font = fonts.get("Pacmania.otf", scaled(h, 48))
        self.selected = 0
        self.options: list[tuple[str, Callable[[], None] | None]] = []
        self.start_y = scaled(h, 200)
        self.step = scaled(h, 80)
        self.keymap = {
            pygame.K_DOWN: lambda: self.move(1),
            pygame.K_UP: lambda: self.move(-1),
        }

    def move(self, d: int) -> None:
        """Move the selection by d, wrapping around."""
        self.selected = (self.selected + d) % len(self.options)

    def labels(self) -> list[str]:
        """Return the option labels."""
        return [label for label, _ in self.options]

    def draw(self, screen: pygame.Surface) -> None:
        """Draw each option, highlighting the selected one."""
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
        """Run the action bound to the pressed key, if any."""
        if event.type != pygame.KEYDOWN:
            return
        action = self.keymap.get(event.key)
        if action:
            action()

    @staticmethod
    def restrict() -> None:
        """No-op used to disable a key binding."""
        pass
