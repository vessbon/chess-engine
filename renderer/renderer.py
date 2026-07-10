import os

import pygame
import pygame.gfxdraw

from board import Board
from chess_types import Color, Coordinate, HighlightType
from constants import (
    BOARD_DIMENSION,
    BOARD_SIZE,
    PIECE_PADDING,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SQUARE_SIZE,
    WIDGET_PADDING,
)
from game import Game

from .widgets import ClockWidget, PlayerWidget

ASSETS_PATH = CHESS_ICONS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets")
)

FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
CHESS_ICONS_PATH = os.path.join(ASSETS_PATH, "icons")

BOARD_LEFT = SCREEN_WIDTH // 2 - BOARD_SIZE // 2
BOARD_TOP = SCREEN_HEIGHT // 2 - BOARD_SIZE // 2

FONT_PATH_DEJA_VU_SANS = os.path.join(FONTS_PATH, "dejavusans.ttf")


class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 100, 255))
        pygame.display.set_caption("Chess")

        self.dark_color = (237, 214, 176)
        self.light_color = (184, 135, 98)

        self.highlights: dict[Coordinate, HighlightType] = {}
        self.moves: set[Coordinate] = set()

        self.player_widget_white = PlayerWidget(
            (BOARD_LEFT, BOARD_TOP + BOARD_SIZE + WIDGET_PADDING),
            FONT_PATH_DEJA_VU_SANS,
            Color.WHITE.value.capitalize(),
            "topleft",
        )
        self.clock_white = ClockWidget(
            (BOARD_LEFT + BOARD_SIZE, BOARD_TOP + BOARD_SIZE + WIDGET_PADDING),
            FONT_PATH_DEJA_VU_SANS,
            0,
            "topright",
        )

        self.player_widget_black = PlayerWidget(
            (BOARD_LEFT, BOARD_TOP - WIDGET_PADDING),
            FONT_PATH_DEJA_VU_SANS,
            Color.BLACK.value.capitalize(),
            "bottomleft",
        )
        self.clock_black = ClockWidget(
            (BOARD_LEFT + BOARD_SIZE, BOARD_TOP - WIDGET_PADDING),
            FONT_PATH_DEJA_VU_SANS,
            0,
            "bottomright",
        )

        self.pieces = self._load_pieces()

    def draw(self, game: Game) -> None:
        surface = self.draw_board()
        self._draw_pieces(surface, game.board)
        self._draw_coordinates(surface)
        self._draw_highlights(surface)
        self._draw_moves(surface)

        self.screen.blit(surface, (BOARD_LEFT, BOARD_TOP))

        self.player_widget_white.draw(self.screen)
        self.player_widget_black.draw(self.screen)

        self.clock_white.draw(self.screen)
        self.clock_black.draw(self.screen)

        pygame.display.update()

    def draw_board(self) -> pygame.Surface:
        surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        surface.fill((255, 255, 255))

        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                color = self.dark_color if (row + col) % 2 == 0 else self.light_color
                pygame.draw.rect(
                    surface,
                    color,
                    (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )

        return surface

    def update_clock(self, time_white: float, time_black: float):
        self.clock_white.set_time(time_white)
        self.clock_black.set_time(time_black)

    def mouse_to_square(self, position: tuple[int, int]) -> Coordinate | None:
        x, y = position

        board_x = SCREEN_WIDTH // 2 - BOARD_SIZE // 2
        board_y = SCREEN_HEIGHT // 2 - BOARD_SIZE // 2

        x -= board_x
        y -= board_y

        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE

        if not self._in_bounds(row, col):
            return

        return (row, col)

    def highlight_square(self, row: int, col: int) -> None:
        self._highlight_square(row, col, HighlightType.NORMAL)

    def highlight_move(
        self, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> None:
        self.clear_highlights(HighlightType.LAST_MOVE)

        self._highlight_square(from_row, from_col, HighlightType.LAST_MOVE)
        self._highlight_square(to_row, to_col, HighlightType.LAST_MOVE)

    def highlight_selection(self, row: int, col: int):
        self.clear_highlights(HighlightType.SELECTED)
        self._highlight_square(row, col, HighlightType.SELECTED)

    def clear_highlights(self, highlight_type: HighlightType) -> None:
        self.highlights = {
            coord: htype
            for coord, htype in self.highlights.items()
            if htype is not highlight_type
        }

    def set_moves(self, moves: set[Coordinate]) -> None:
        if moves == self.moves:
            self.moves.clear()
        else:
            self.moves.clear()
            self.moves.update(moves)

    def _draw_coordinates(self, surface: pygame.Surface):
        font_size = 16
        padding = 5

        font = pygame.font.Font(FONT_PATH_DEJA_VU_SANS, font_size)

        files = "abcdefgh"

        for square in range(BOARD_DIMENSION):
            number = str(8 - square)
            letter = files[square]

            numbers = font.render(
                number, True, self.light_color if square % 2 == 0 else self.dark_color
            )
            letters = font.render(
                letter, True, self.dark_color if square % 2 == 0 else self.light_color
            )

            surface.blit(numbers, (padding, square * SQUARE_SIZE + padding))
            surface.blit(
                letters,
                (
                    (square + 1) * SQUARE_SIZE - (font_size),
                    BOARD_DIMENSION * SQUARE_SIZE - (font_size + padding),
                ),
            )

    def _draw_pieces(self, surface: pygame.Surface, board: Board) -> None:
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                piece = board.get(row, col)
                if piece is None:
                    continue

                piece_image = self.pieces[
                    f"{piece.color.value}_{piece.symbol.capitalize()}"
                ]

                piece_rect = piece_image.get_rect(
                    center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                )

                surface.blit(piece_image, piece_rect)

    def _draw_highlights(self, surface: pygame.Surface) -> None:
        colors = {
            HighlightType.NORMAL: (255, 0, 0, 80),
            HighlightType.CAPTURE: (255, 0, 0, 80),
            HighlightType.LAST_MOVE: (0, 255, 0, 80),
            HighlightType.SELECTED: (255, 255, 0, 80),
        }

        for (row, col), highlight_type in self.highlights.items():
            rect = pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
            )

            highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
            highlight.fill(colors[highlight_type])

            surface.blit(highlight, rect)

    def _draw_moves(self, surface: pygame.Surface) -> None:
        radius = SQUARE_SIZE // 6
        cx = SQUARE_SIZE // 2
        cy = SQUARE_SIZE // 2

        for row, col in self.moves:
            move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            color = (0, 0, 0, 100)

            pygame.gfxdraw.aacircle(move_surface, cx, cy, radius, color)
            pygame.gfxdraw.filled_circle(move_surface, cx, cy, radius, color)

            surface.blit(move_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def _load_pieces(self) -> dict[str, pygame.Surface]:
        pieces = {}

        colors = [Color.WHITE.value, Color.BLACK.value]
        types: list[str] = ["K", "Q", "R", "B", "N", "P"]

        for color in colors:
            for piece_type in types:
                name = f"{color}_{piece_type}"
                path = os.path.join(CHESS_ICONS_PATH, f"{color}-{piece_type}.png")

                pieces[name] = self._load_piece(path, SQUARE_SIZE)

        return pieces

    def _load_piece(self, path: str, size: int) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(
            image, (size - PIECE_PADDING, size - PIECE_PADDING)
        )

    def _highlight_square(
        self, row: int, col: int, highlight_type: HighlightType
    ) -> None:
        if not self._in_bounds(row, col):
            return

        coord = (row, col)
        current = self.highlights.get(coord)

        if highlight_type is HighlightType.NORMAL:
            if current is HighlightType.NORMAL:
                del self.highlights[coord]
                return

            if current is not None:
                return

        self.highlights[coord] = highlight_type

    def _set_highlight(self, row: int, col: int, highlight_type: HighlightType) -> None:
        if not self._in_bounds(row, col):
            return

        self.highlights[(row, col)] = highlight_type

    def _in_bounds(self, row: int, col: int) -> bool:
        if 0 <= row < BOARD_DIMENSION and 0 <= col <= BOARD_DIMENSION:
            return True
        return False
