from .piece import Piece


class Knight(Piece):
    def symbol(self):
        return "N" if self.color == "white" else "n"

    def moves(self, position, board):
        row, col = position

        OFFSETS = (
            (2, -1),
            (2, 1),
            (-2, -1),
            (-2, 1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        )

        moves = []

        for offset in OFFSETS:
            dr, dc = offset

            move = (row + dr, col + dc)
            occupant = board.get(*move)

            if occupant and occupant.color == self.color:
                continue

            moves.append((row + dr, col + dc))

        return moves
