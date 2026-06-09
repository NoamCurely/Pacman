import pygame
from src.fonts import Fonts
from src.parsing import Config
from src.scenes.scene import Scene
from src.ui.hud import Hud
from src.game.maze import Maze, BG_COLOR
from src.game.pacman import Pacman
from src.game.gum import Gum
from src.game.ghost import Ghost
from src.game.spawn import Spawn
from src.sounds import sfx


class Game(Scene):
    """Scène de jeu: labyrinthe du niveau courant + bandeau HUD en bas."""

    def __init__(self, fonts: Fonts, screen_rect: pygame.Rect,
                 config: Config, cheat: bool = False) -> None:
        super().__init__()
        self.fonts = fonts
        self.screen_rect = screen_rect
        self.config = config
        self.cheat = cheat
        self.invincible = False
        self.noclip = False

        h = screen_rect.height
        hud_h = round(h * 40 / 720)
        panel_w = 140 if cheat else 0
        self.maze_area = pygame.Rect(
            0, 0, screen_rect.width - panel_w, h - hud_h)
        self.hud_area = pygame.Rect(
            0, h - hud_h, screen_rect.width, hud_h)
        self.cheat_panel = pygame.Rect(
            screen_rect.width - panel_w, 0, panel_w, h - hud_h)
        self.hud = Hud(
            fonts, self.hud_area,
            {"invincible": False, "noclip": False} if cheat else None)

        self.score = 0
        self.lives = config.lives
        self.time_left = config.level_max_time
        self.start_ticks = pygame.time.get_ticks()
        self.dying = False
        self.death_idx = 0
        self.death_last = 0
        self.ghosts_hidden = False
        self.ghost_respawn_at = 0
        self.levels = 0
        self.speed = 2.0
        self.build_level()

        sfx.play("pacman_beginning.wav")

    DEATH_FRAME_MS = 150

    def update(self) -> None:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.time_left = max(0, self.config.level_max_time - elapsed)
        if self.time_left == 0:
            from src.scenes.gameover import GameOver
            self.next_scene = GameOver(
                self.fonts, self.screen_rect, self.config, self.score)
            return

        if self.dying:
            self.animate_death()
            return
        if self.ghosts_hidden and \
                pygame.time.get_ticks() >= self.ghost_respawn_at:
            for ghost in self.ghosts:
                ghost.reset(self.maze_area)
            self.ghosts_hidden = False

        self.pacman.update(self.maze, self.maze_area, self.noclip)
        cell = self.maze.cell_at(
            self.pacman.pos.x,
            self.pacman.pos.y,
            self.maze_area
        )
        is_super = cell in self.gum.super_gum
        gained = self.gum.eat(cell)
        self.score += gained
        if is_super:
            sfx.play("pacman_eatfruit.wav")
        elif gained > 0:
            sfx.play("pacman_chomp.wav")

        if self.gum.remaining() == 0 and len(self.gum.super_gum) == 0:
            self.next_level()
            return

        if self.ghosts_hidden:
            return

        for ghost in self.ghosts:
            ghost.update(self.maze, self.maze_area, cell,
                         self.pacman.direction)
        if is_super:
            for ghost in self.ghosts:
                ghost.set_frightened()

        for ghost in self.ghosts:
            if ghost.dead:
                continue
            gcell = self.maze.cell_at(
                ghost.pos.x, ghost.pos.y, self.maze_area)
            if gcell != cell:
                continue
            if ghost.frightened:
                self.score += self.config.points_per_ghost
                sfx.play("pacman_eatghost.wav")
                ghost.eaten(self.maze_area)
            elif not self.invincible:
                self.start_death()
                break

    def start_death(self) -> None:
        """Lance l'animation de mort (gèle le jeu)."""
        self.dying = True
        self.death_idx = 0
        self.death_last = pygame.time.get_ticks()
        sfx.play("pacman_death.wav")

    def animate_death(self) -> None:
        """Avance les frames de mort ; à la fin -> lose_life."""
        now = pygame.time.get_ticks()
        if now - self.death_last >= self.DEATH_FRAME_MS:
            self.death_idx += 1
            self.death_last = now
            if self.death_idx >= len(self.pacman.death_frames):
                self.dying = False
                self.lose_life()

    def build_level(self) -> None:
        level = self.config.levels[self.levels]
        self.maze = Maze(
            level.width,
            level.height,
            seed=self.config.seed
            )
        self.pacman = Pacman(self.maze, self.config, self.maze_area)
        x, y = self.maze.find_open_cell(self.maze_area)
        self.pacman.pos = pygame.Vector2(x, y)
        spawn_cell = self.maze.cell_at(x, y, self.maze_area)
        self.spawn = Spawn(self.maze)
        ghost_cells = set(self.spawn.ghost_spawns())
        self.gum = Gum(self.maze, self.config, ghost_cells, spawn_cell)
        self.ghosts = [Ghost(self.maze, n, self.speed)
                       for n in ("blinky", "pinky", "inky", "clyde")]
        self.spawn.random_ghost(self.ghosts)
        for ghost in self.ghosts:
            ghost.reset(self.maze_area)

    def next_level(self) -> None:
        self.levels += 1
        if self.levels >= len(self.config.levels):
            from src.scenes.victory import Victory
            self.next_scene = Victory(
                self.fonts, self.screen_rect, self.config, self.score)
            return
        self.speed += 0.2
        self.start_ticks = pygame.time.get_ticks()
        self.build_level()

    def lose_life(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            from src.scenes.gameover import GameOver
            self.next_scene = GameOver(
                self.fonts, self.screen_rect, self.config, self.score)
            return
        self.respawn()

    def respawn(self) -> None:
        sx, sy = self.maze.find_open_cell(self.maze_area)
        self.pacman.pos = pygame.Vector2(sx, sy)
        self.pacman.vel = pygame.Vector2(0, 0)
        self.pacman.queued_dir = None
        self.ghosts_hidden = True
        self.ghost_respawn_at = pygame.time.get_ticks() + 5000

    def handle_event(self, event: pygame.event.Event) -> None:
        self.pacman.handle_event(event)
        if not self.cheat or event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_i:
            self.invincible = not self.invincible
        if event.key == pygame.K_n:
            self.noclip = not self.noclip
        if event.key == pygame.K_f:
            for ghost in self.ghosts:
                ghost.set_frightened()
        if event.key == pygame.K_g:
            self.gum.gum.clear()
            self.gum.super_gum.clear()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        self.maze.draw(screen, self.maze_area)
        self.gum.draw(screen, self.maze_area, self.maze)
        if not self.dying and not self.ghosts_hidden:
            for ghost in self.ghosts:
                ghost.draw(screen, self.maze_area)
        self.hud.draw(screen, self.hud_area,
                      self.score, self.lives, self.time_left,
                      self.levels + 1)
        if self.cheat:
            self.hud.draw_cheat(
                screen, self.cheat_panel,
                {"invincible": self.invincible, "noclip": self.noclip})

        if self.dying:
            idx = min(self.death_idx, len(self.pacman.death_frames) - 1)
            sprite = self.pacman.death_frames[idx]
        else:
            sprite = self.pacman.pac
        pac_rect = sprite.get_rect(center=(int(self.pacman.pos.x),
                                           int(self.pacman.pos.y)))
        screen.blit(sprite, pac_rect)
