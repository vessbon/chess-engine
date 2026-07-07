from .config import DIAGONAL_DIRECTIONS
from .piece import Piece

from chess_types import Color


class Bishop(Piece):
    VALUE = 3

    @property
    def symbol(self):
        return "B" if self.color == Color.WHITE else "b"

    def moves(self, square, board):
        return self._sliding_moves(square, board, DIAGONAL_DIRECTIONS)
