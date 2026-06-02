import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene
from src.ui.confirm import ConfirmDialog


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
        h = screen_rect.height
        self.start_y = round(h * 120 / 720)
        self.step = round(h * 70 / 720)
        self.value_font = pygame.font.Font(None, round(h * 60 / 720))
        self.hint_size = round(h * 28 / 720)
        self.hint_font = pygame.font.SysFont("dejavusans", self.hint_size)
        self.hint_font_bold = pygame.font.SysFont(
            "dejavusans", self.hint_size, bold=True)
        self.confirming = False
        self.dialog = ConfirmDialog(self.font, self.hint_font)
        # auto-répétition des touches maintenues (global pygame)
        pygame.key.set_repeat(350, 60)
        self.enter_held = False  # bloque répétition d'ENTER
        self.keymap[pygame.K_RIGHT] = lambda: self.adjust(1)
        self.keymap[pygame.K_LEFT] = lambda: self.adjust(-1)
        self.keymap[pygame.K_RETURN] = self.ask_confirm
        self.keymap[pygame.K_ESCAPE] = self.back
        self.normal_keymap = self.keymap
        self.confirm_keymap = {
            pygame.K_RETURN: self.do_save,
            pygame.K_ESCAPE: self.cancel,
        }

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            self.enter_held = False
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.enter_held:
                return  # ignore répétition d'ENTER
            self.enter_held = True
        super().handle_event(event)

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
        pygame.key.set_repeat()  # coupe répétition en sortant
        from src.scenes.game import Game
        self.next_scene = Game(self.fonts, self.screen_rect, self.config)

    def back(self) -> None:
        pygame.key.set_repeat()  # coupe répétition en sortant
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
            gap = round(self.screen_rect.height * 15 / 720)
            val_rect = val.get_rect(
                midleft=(name_rect.right + gap, name_rect.centery))
            screen.blit(val, val_rect)

        key_color = (140, 140, 140)
        txt_color = (120, 120, 120)
        groups = [
            ("↑↓", "choice"),
            ("←→", "update"),
            ("ENTER", "valid"),
            ("ESC", "back"),
        ]
        h = self.screen_rect.height
        key_gap = round(h * 8 / 720)     # entre touche et son mot
        group_gap = round(h * 28 / 720)  # entre deux groupes
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
        y = self.screen_rect.bottom - round(h * 40 / 720)
        for ks, ts in rendered:
            screen.blit(ks, (x, y - ks.get_height() // 2))
            x += ks.get_width() + key_gap
            screen.blit(ts, (x, y - ts.get_height() // 2))
            x += ts.get_width() + group_gap

        if self.confirming:
            self.dialog.draw(screen, self.screen_rect,
                             "SAVE CONFIG?", "ENTER     ESC ")
