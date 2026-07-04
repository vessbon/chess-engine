from .piece import Piece


class Pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def symbol(self):
        return "P" if self.color == "white" else "p"

    def moves(self, position, board):
        return [(1, 2)]
