import pygame


class Scene:
    def __init__(self) -> None:
        self.next_scene: "Scene | None" = None
        self.should_quit: bool = False

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass
