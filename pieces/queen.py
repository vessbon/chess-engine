from .config import directions
from .piece import Piece


class Queen(Piece):
    def symbol(self):
        return "Q" if self.color == "white" else "q"

    def moves(self, position, board):
        row, col = position

        moves = []

        for dr, dc in directions:
            next_row = row + dr
            next_col = col + dc

            while board.in_bounds(next_row, next_col):
                move = (next_row, next_col)
                occupant = board.get(*move)

                if occupant and occupant.color == self.color:
                    break

                moves.append(move)

                if occupant:
                    break

                next_row += dr
                next_col += dc

        return moves
