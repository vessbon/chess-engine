import os

import pygame

from board import Board
from chess_types import Color
from constants import (
    BOARD_DIMENSION,
    BOARD_SIZE,
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
        self.pieces = self._load_pieces()

    def draw(self, game: Game) -> None:
        surface = self.draw_board()
        self.draw_pieces(surface, game.board)
        self.draw_coordinates(surface)

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

    def draw_coordinates(self, surface: pygame.Surface):
        padding = 5
        font_size = 16
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

    def draw_pieces(self, surface: pygame.Surface, board: Board) -> None:
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                piece = board.get(row, col)
                if piece is None:
                    continue

                surface.blit(
                    self.pieces[f"{piece.color.value}_{piece.symbol.capitalize()}"],
                    (col * SQUARE_SIZE, row * SQUARE_SIZE),
                )

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
        return pygame.transform.smoothscale(image, (size - 5, size - 5))
