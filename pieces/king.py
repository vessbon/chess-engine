from .config import directions
from .piece import Piece


class King(Piece):
    def symbol(self):
        return "K" if self.color == "white" else "k"

    def moves(self, position, board):
        row, col = position

        moves = []

        for direction in directions:
            dr, dc = direction
            move = (row + dr, col + dc)

            occupant = board.get(*move)
            if occupant and occupant.color == self.color:
                continue

            moves.append(move)

        return moves
