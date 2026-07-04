from .config import DIAGONAL_DIRECTIONS
from .piece import Piece


class Bishop(Piece):
    def symbol(self):
        return "B" if self.color == "white" else "b"

    def moves(self, position, board):
        return self._sliding_moves(position, board, DIAGONAL_DIRECTIONS)
