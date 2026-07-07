from chess_types import Color

from .config import STRAIGHT_DIRECTIONS
from .piece import Piece


class Rook(Piece):
    VALUE = 5

    @property
    def symbol(self):
        return "R" if self.color == Color.WHITE else "r"

    def moves(self, square, board):
        return self._sliding_moves(square, board, STRAIGHT_DIRECTIONS)
