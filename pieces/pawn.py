from .piece import Piece


class Pawn(Piece):
    def symbol(self):
        return "P" if self.color == "white" else "p"

    def moves(self, position):
        row = position[0]
        col = position[1]

        if self.color == "white":
            move_distance = 2 if row == 6 else 1
            return [(row - move_distance, col)]
        else:
            move_distance = 2 if row == 1 else 1
            return [(row + move_distance, col)]
