from chess_types import Color

from .config import ALL_DIRECTIONS
from .piece import Piece


class Queen(Piece):
    VALUE = 9

    @property
    def symbol(self):
        return "Q" if self.color == Color.WHITE else "q"

    def moves(self, square, board):
        return self._sliding_moves(square, board, ALL_DIRECTIONS)
