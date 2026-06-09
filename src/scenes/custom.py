"""Custom: edit config values in place before starting a game."""
import pygame

from src.fonts import Fonts
from src.parsing import Config
from src.scenes.menu import Menu
from src.scenes.scene import Scene, scaled
from src.ui.confirm import ConfirmDialog


class Custom(Menu):
    """Editable list of config fields with a save confirmation."""

    def __init__(
        self,
        fonts: Fonts,
        screen_rect: pygame.Rect,
        config: Config,
        previous: Scene
    ) -> None:
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
        self.start_y = scaled(h, 120)
        self.step = scaled(h, 70)
        self.value_font = pygame.font.Font(None, scaled(h, 60))
        self.hint_size = scaled(h, 28)
        self.hint_font = pygame.font.SysFont("dejavusans", self.hint_size)
        self.hint_font_bold = pygame.font.SysFont(
            "dejavusans", self.hint_size, bold=True)
        self.confirming = False
        self.dialog = ConfirmDialog(self.font, self.hint_font)
        pygame.key.set_repeat(350, 60)
        self.enter_held = False
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
        """Debounce ENTER auto-repeat, then dispatch to the menu."""
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            self.enter_held = False
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.enter_held:
                return
            self.enter_held = True
        super().handle_event(event)

    def adjust(self, delta: int) -> None:
        """Change the selected field by delta, keeping it positive."""
        key = self.fields[self.selected]
        val = self.draft[key] + delta
        if val > 0:
            self.draft[key] = val

    def ask_confirm(self) -> None:
        """Open the save confirmation prompt."""
        self.confirming = True
        self.keymap = self.confirm_keymap

    def cancel(self) -> None:
        """Close the confirmation prompt."""
        self.confirming = False
        self.keymap = self.normal_keymap

    def do_save(self) -> None:
        """Apply the edited values to the config and start a game."""
        for k, v in self.draft.items():
            setattr(self.config, k, v)
        self.cancel()
        pygame.key.set_repeat()
        from src.scenes.game import Game
        self.next_scene = Game(self.fonts, self.screen_rect, self.config)

    def back(self) -> None:
        """Return to the previous scene."""
        pygame.key.set_repeat()
        self.next_scene = self.previous

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the editable fields, the key hints and the dialog."""
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
            gap = scaled(self.screen_rect.height, 15)
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
        key_gap = scaled(h, 8)
        group_gap = scaled(h, 28)
        rendered = [
            (self.hint_font_bold.render(k, True, key_color),
             self.hint_font.render(t, True, txt_color))
            for k, t in groups
        ]
        total = sum(ks.get_width() + key_gap + ts.get_width()
                    for ks, ts in rendered)
        total += group_gap * (len(rendered) - 1)
        x = cx - total // 2
        y = self.screen_rect.bottom - scaled(h, 40)
        for ks, ts in rendered:
            screen.blit(ks, (x, y - ks.get_height() // 2))
            x += ks.get_width() + key_gap
            screen.blit(ts, (x, y - ts.get_height() // 2))
            x += ts.get_width() + group_gap

        if self.confirming:
            self.dialog.draw(screen, self.screen_rect,
                             "SAVE CONFIG?", "ENTER     ESC ")
