from .config import ALL_DIRECTIONS
from .piece import Piece


class Queen(Piece):
    VALUE = 9

    @property
    def symbol(self):
        return "Q" if self.color == "white" else "q"

    def moves(self, position, board):
        return self._sliding_moves(position, board, ALL_DIRECTIONS)
