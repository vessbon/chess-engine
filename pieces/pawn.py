from .piece import Piece


class Pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def symbol(self) -> str:
        return "P" if self.color == "white" else "p"
