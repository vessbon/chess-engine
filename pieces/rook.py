from chess_types import Color

from .config import STRAIGHT_DIRECTIONS
from .piece import Piece


class Rook(Piece):
    VALUE = 5

    @property
    def symbol(self):
        return "R" if self.color == Color.WHITE else "r"

    def moves(self, position, board):
        return self._sliding_moves(position, board, STRAIGHT_DIRECTIONS)
