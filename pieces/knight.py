from chess_types import Color

from .piece import Piece


class Knight(Piece):
    VALUE = 3

    @property
    def symbol(self):
        return "N" if self.color == Color.WHITE else "n"

    def moves(self, square, board):
        offsets = (
            (2, -1),
            (2, 1),
            (-2, -1),
            (-2, 1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        )

        return self._stepping_moves(square, board, offsets)
