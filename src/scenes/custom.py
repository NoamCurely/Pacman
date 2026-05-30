import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene


class Custom(Menu):
    """Édite la config: ←/→ ajuste un brouillon, ENTER applique, ESC retour."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, previous: Scene) -> None:
        super().__init__(fonts, screen_rect, config)
        self.previous = previous
        self.fields = [
            "lives",
            "pacgum",
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost",
            "seed",
            "level_max_time",
        ]
        self.options = [(f, None) for f in self.fields]
        self.draft = {k: getattr(config, k) for k in self.fields}
        self.start_y = 120
        self.step = 70
        self.value_font = pygame.font.Font(None, 60)
        self.hint_size = 28
        self.hint_font = pygame.font.SysFont("dejavusans", self.hint_size)
        self.hint_font_bold = pygame.font.SysFont(
            "dejavusans", self.hint_size, bold=True)
        self.confirming = False
        self.keymap[pygame.K_RIGHT] = lambda: self.adjust(1)
        self.keymap[pygame.K_LEFT] = lambda: self.adjust(-1)
        self.keymap[pygame.K_RETURN] = self.ask_confirm
        self.keymap[pygame.K_ESCAPE] = self.back
        self.normal_keymap = self.keymap
        self.confirm_keymap = {
            pygame.K_RETURN: self.do_save,
            pygame.K_ESCAPE: self.cancel,
        }

    def adjust(self, delta: int) -> None:
        key = self.fields[self.selected]
        val = self.draft[key] + delta
        if val > 0:
            self.draft[key] = val

    def ask_confirm(self) -> None:
        self.confirming = True
        self.keymap = self.confirm_keymap

    def cancel(self) -> None:
        self.confirming = False
        self.keymap = self.normal_keymap

    def do_save(self) -> None:
        for k, v in self.draft.items():
            setattr(self.config, k, v)
        self.cancel()

    def back(self) -> None:
        self.next_scene = self.previous

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        cx = self.screen_rect.centerx
        for i, k in enumerate(self.fields):
            color: str | tuple[int, int, int]
            if i == self.selected:
                color = "yellow"
            else:
                color = (120, 120, 120)
            name = self.font.render(k.upper(), True, color)
            val = self.value_font.render(str(self.draft[k]), True, color)
            y = self.start_y + i * self.step
            name_rect = name.get_rect(center=(cx, y))
            screen.blit(name, name_rect)
            val_rect = val.get_rect(
                midleft=(name_rect.right + 15, name_rect.centery))
            screen.blit(val, val_rect)

        key_color = (140, 140, 140)
        txt_color = (120, 120, 120)
        groups = [
            ("↑↓", "choice"),
            ("←→", "update"),
            ("ENTER", "valid"),
            ("ESC", "back"),
        ]
        key_gap = 8     # entre touche et son mot
        group_gap = 28  # entre deux groupes
        # pré-rend (touche bold, mot normal) par groupe
        rendered = [
            (self.hint_font_bold.render(k, True, key_color),
             self.hint_font.render(t, True, txt_color))
            for k, t in groups
        ]
        total = sum(ks.get_width() + key_gap + ts.get_width()
                    for ks, ts in rendered)
        total += group_gap * (len(rendered) - 1)
        x = cx - total // 2
        y = self.screen_rect.bottom - 40
        for ks, ts in rendered:
            screen.blit(ks, (x, y - ks.get_height() // 2))
            x += ks.get_width() + key_gap
            screen.blit(ts, (x, y - ts.get_height() // 2))
            x += ts.get_width() + group_gap

        if self.confirming:
            box = self.font.render("SAVE CONFIG?", True, "yellow")
            screen.blit(box, box.get_rect(center=self.screen_rect.center))
            ask = self.hint_font.render(
                "ENTER = yes     ESC = no", True, (200, 200, 200))
            screen.blit(ask, ask.get_rect(
                center=(cx, self.screen_rect.centery + 50)))
