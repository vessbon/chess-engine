from chess_types import Color

from .piece import Piece


class Pawn(Piece):
    VALUE = 1

    @property
    def symbol(self):
        return "P" if self.color == Color.WHITE else "p"

    def moves(self, position, board):
        row, col = position

        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1

        moves = []

        one_step = (row + direction, col)

        # Normal movement
        if board.in_bounds(*one_step) and board.is_empty(*one_step):
            moves.append(one_step)

            two_steps = (row + direction * 2, col)
            if (
                row == start_row
                and board.in_bounds(*two_steps)
                and board.is_empty(*two_steps)
            ):
                moves.append(two_steps)

        # Capture movement
        for dc in (1, -1):
            diagonal_step = (one_step[0], one_step[1] + dc)
            if not board.in_bounds(*diagonal_step):
                continue
            occupant = board.get(*diagonal_step)
            if occupant and occupant.color != self.color:
                moves.append(diagonal_step)

        return moves
