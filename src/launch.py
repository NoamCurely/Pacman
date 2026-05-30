import pygame
from src.parsing import Config
from src.fonts import Fonts
from src.scenes.scene import Scene
from src.scenes.landing import Landing


class Launch:
    def __init__(self, config: Config) -> None:
        self.config = config

    def menu(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode(
            (1280, 720), pygame.SCALED | pygame.FULLSCREEN)
        clock = pygame.time.Clock()

        fonts = Fonts()
        scene: Scene = Landing(fonts, screen.get_rect(), self.config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    scene.handle_event(event)

            scene.update()
            scene.draw(screen)
            pygame.display.flip()
            clock.tick(60)

            if scene.should_quit:
                running = False
            elif scene.next_scene is not None:
                nxt = scene.next_scene
                scene.next_scene = None
                scene = nxt
        pygame.quit()
