from math import inf as infinity

from chess_types import Color

from .config import ALL_DIRECTIONS
from .piece import Piece


class King(Piece):
    VALUE = infinity

    @property
    def symbol(self):
        return "K" if self.color == Color.WHITE else "k"

    def moves(self, position, board):
        return self._stepping_moves(position, board, ALL_DIRECTIONS)
