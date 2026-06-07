import pygame

from mazegenerator import MazeGenerator

BG_COLOR = (25, 25, 30)
WALL_COLOR = (240, 240, 240)
WALL_W = 4


class Maze:
    def __init__(self, width: int, height: int, seed: int = 0) -> None:
        gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        self.grid: list[list[int]] = gen.maze
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def draw(self, screen: pygame.Surface,
             area: pygame.Rect | None = None) -> None:
        if area is None:
            area = screen.get_rect()
        cell_size, offset_x, offset_y = self._geometry(area)

        for y in range(self.rows):
            for x in range(self.cols):
                v = self.grid[y][x]
                left = offset_x + x * cell_size
                top = offset_y + y * cell_size
                right, bottom = left + cell_size, top + cell_size
                north = v & 1
                east = v & 2
                south = v & 4
                west = v & 8

                if north:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (left, top), (right, top), WALL_W)
                if east:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (right, top), (right, bottom), WALL_W)
                if south:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (left, bottom), (right, bottom), WALL_W)
                if west:
                    pygame.draw.line(screen, WALL_COLOR,
                                     (left, top), (left, bottom), WALL_W)
                if v == 15:
                    pygame.draw.rect(screen, (60, 90, 200),
                                     (left, top, cell_size, cell_size))

    def _geometry(self, area: pygame.Rect) -> tuple[int, int, int]:
        """Return (cell_size, offset_x, offset_y) for the draw area."""
        size = min(area.width // self.cols, area.height // self.rows)
        offset_x = area.x + (area.width - self.cols * size) // 2
        offset_y = area.y + (area.height - self.rows * size) // 2
        return size, offset_x, offset_y

    def corner_cells(self) -> set[tuple[int, int]]:
        """Return the four corner cells (col, row) of the maze grid."""
        return {
            (0, 0),
            (self.cols - 1, 0),
            (0, self.rows - 1),
            (self.cols - 1, self.rows - 1),
        }

    def cell_size(self, area: pygame.Rect) -> int:
        """Return pixel size of one cell for the given draw area."""
        return self._geometry(area)[0]

    def cell_center(self, col: int, row: int,
                    area: pygame.Rect) -> tuple[int, int]:
        """Return pixel center of cell (col, row) within area."""
        size, offset_x, offset_y = self._geometry(area)
        return (offset_x + col * size + size // 2,
                offset_y + row * size + size // 2)

    def cell_at(self, px: float, py: float,
                area: pygame.Rect) -> tuple[int, int]:
        """Return (col, row) of the cell containing pixel (px, py)."""
        size, offset_x, offset_y = self._geometry(area)
        return (int((px - offset_x) // size),
                int((py - offset_y) // size))

    def is_wall(self, px: float, py: float,
                dx: float, dy: float,
                area: pygame.Rect) -> bool:
        col0, row0 = self.cell_at(px, py, area)

        WALL_MARGIN = 10
        nx = px + dx + (WALL_MARGIN if dx > 0 else -
                        WALL_MARGIN if dx < 0 else 0)
        ny = py + dy + (WALL_MARGIN if dy > 0 else -
                        WALL_MARGIN if dy < 0 else 0)
        col1, row1 = self.cell_at(nx, ny, area)

        if not (0 <= row1 < self.rows and 0 <= col1 < self.cols):
            return True
        if col0 == col1 and row0 == row1:
            return False

        v_src = self.grid[row0][col0]
        v_dst = self.grid[row1][col1]

        if (col1 > col0):
            return bool(v_src & 2) or bool(v_dst & 8)
        if (col1 < col0):
            return bool(v_src & 8) or bool(v_dst & 2)
        if (row1 > row0):
            return bool(v_src & 4) or bool(v_dst & 1)
        if (row1 < row0):
            return bool(v_src & 1) or bool(v_dst & 4)

        return False

    def find_open_cell(self, area: pygame.Rect) -> tuple[float, float]:
        """Return pixel center of the most open cell nearest the middle."""
        best = (self.cols // 2, self.rows // 2)
        best_walls = 5
        best_dist = self.cols + self.rows
        center_col, center_row = self.cols // 2, self.rows // 2
        for row in range(self.rows):
            for col in range(self.cols):
                v = self.grid[row][col]
                walls = bin(v).count('1')
                dist = abs(col - center_col) + abs(row - center_row)
                if walls < best_walls or (walls == best_walls
                                          and dist < best_dist):
                    best_walls = walls
                    best_dist = dist
                    best = (col, row)

        col, row = best
        return self.cell_center(col, row, area)
