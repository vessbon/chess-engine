import os

import pygame
import pygame.gfxdraw

from board import Board
from chess_types import Color, Coordinate
from constants import (
    BOARD_DIMENSION,
    BOARD_SIZE,
    CAPTURE_RGB,
    PIECE_PADDING,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SQUARE_SIZE,
)
from game import Game

ASSETS_PATH = CHESS_ICONS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets")
)

FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
CHESS_ICONS_PATH = os.path.join(ASSETS_PATH, "icons")


class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 100, 255))
        pygame.display.set_caption("Chess")

        self.dark_color = (237, 214, 176)
        self.light_color = (184, 135, 98)

        self.highlights: set[Coordinate] = set()
        self.moves: set[Coordinate] = set()

        self.pieces = self._load_pieces()

    def draw(self, game: Game) -> None:
        surface = self.draw_board()
        self._draw_pieces(surface, game.board)
        self._draw_coordinates(surface)
        self._draw_highlights(surface)
        self._draw_moves(surface)

        self.screen.blit(
            surface,
            (SCREEN_WIDTH / 2 - BOARD_SIZE / 2, SCREEN_HEIGHT / 2 - BOARD_SIZE / 2),
        )

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
        if not self._in_bounds(row, col):
            return

        if (row, col) in self.highlights:
            self.highlights.discard((row, col))
        else:
            self.highlights.add((row, col))

    def set_moves(self, moves: set[Coordinate]) -> None:
        if moves == self.moves:
            self.moves.clear()
        else:
            self.moves.clear()
            self.moves.update(moves)

    def _draw_coordinates(self, surface: pygame.Surface):
        font_size = 16
        padding = 5

        font = pygame.font.Font(os.path.join(FONTS_PATH, "dejavusans.ttf"), font_size)
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
        for row, col in self.highlights:
            rect = pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
            )

            highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
            highlight.fill((*CAPTURE_RGB, 80))

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

    def _in_bounds(self, row: int, col: int) -> bool:
        if 0 <= row < BOARD_DIMENSION and 0 <= col <= BOARD_DIMENSION:
            return True
        return False
