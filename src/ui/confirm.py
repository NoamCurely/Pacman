import pygame


class ConfirmDialog:
    """Modal de confirmation: voile sombre + panneau + titre + indice.

    Composant de dessin pur, réutilisable. La scène garde son état
    (ouvert/fermé) et sa gestion clavier.
    """

    def __init__(self, title_font: pygame.font.Font,
                 hint_font: pygame.font.Font,
                 dim_alpha: int = 200,
                 panel_color: tuple[int, int, int] = (20, 20, 20),
                 border_color: str | tuple[int, int, int] = "yellow",
                 title_color: str | tuple[int, int, int] = "yellow",
                 hint_color: tuple[int, int, int] = (200, 200, 200),
                 pad: int = 40,
                 gap: int = 50,
                 border_width: int = 3,
                 radius: int = 12) -> None:
        self.title_font = title_font
        self.hint_font = hint_font
        self.dim_alpha = dim_alpha
        self.panel_color = panel_color
        self.border_color = border_color
        self.title_color = title_color
        self.hint_color = hint_color
        self.pad = pad
        self.gap = gap
        self.border_width = border_width
        self.radius = radius

    def draw(self, screen: pygame.Surface, rect: pygame.Rect,
             title: str, hint: str) -> None:
        # voile sombre plein écran
        dim = pygame.Surface(rect.size, pygame.SRCALPHA)
        dim.fill((0, 0, 0, self.dim_alpha))
        screen.blit(dim, rect.topleft)

        title_surf = self.title_font.render(title, True, self.title_color)
        title_rect = title_surf.get_rect(center=rect.center)
        hint_surf = self.hint_font.render(hint, True, self.hint_color)
        hint_rect = hint_surf.get_rect(
            center=(rect.centerx, rect.centery + self.gap))

        # panneau opaque derrière le texte
        panel = title_rect.union(hint_rect).inflate(self.pad * 2, self.pad * 2)
        pygame.draw.rect(screen, self.panel_color, panel,
                         border_radius=self.radius)
        pygame.draw.rect(screen, self.border_color, panel,
                         width=self.border_width, border_radius=self.radius)

        screen.blit(title_surf, title_rect)
        screen.blit(hint_surf, hint_rect)
