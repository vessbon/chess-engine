from .piece import Piece


class Knight(Piece):
    VALUE = 3

    @property
    def symbol(self):
        return "N" if self.color == "white" else "n"

    def moves(self, position, board):
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

        return self._stepping_moves(position, board, offsets)
