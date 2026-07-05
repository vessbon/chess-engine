from math import inf as infinity

from .config import ALL_DIRECTIONS
from .piece import Piece


class King(Piece):
    VALUE = infinity

    @property
    def symbol(self):
        return "K" if self.color == "white" else "k"

    def moves(self, position, board):
        row, col = position

        moves = []

        for direction in ALL_DIRECTIONS:
            dr, dc = direction
            move = (row + dr, col + dc)

            occupant = board.get(*move)
            if occupant and occupant.color == self.color:
                continue

            moves.append(move)

        return moves
