"""Scene: base class for all game scenes."""
import pygame

BASE_HEIGHT = 720


def scaled(h: int, px: int) -> int:
    """Scale a 720p-reference pixel value to a screen of height h."""
    return round(h * px / BASE_HEIGHT)


class Scene:
    """Base scene with transition and quit flags; subclasses override."""

    def __init__(self) -> None:
        self.next_scene: "Scene | None" = None
        self.should_quit: bool = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a single input event."""
        pass

    def update(self) -> None:
        """Advance the scene by one frame."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Render the scene onto screen."""
        pass
