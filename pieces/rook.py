from .config import STRAIGHT_DIRECTIONS
from .piece import Piece


class Rook(Piece):
    def symbol(self):
        return "R" if self.color == "white" else "r"

    def moves(self, position, board):
        return self._sliding_moves(position, board, STRAIGHT_DIRECTIONS)
