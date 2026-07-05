from typing import List, Optional

from chess_types import Coordinate
from pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self) -> None:
        self.size = 8
        self.grid: List[List[Optional[Piece]]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]

    def setup(self) -> None:
        self.reset()

        back_rank: List[type[Piece]] = [
            Rook,
            Knight,
            Bishop,
            Queen,
            King,
            Bishop,
            Knight,
            Rook,
        ]

        for i in range(self.size):
            self.set(1, i, Pawn(color="black"))
            self.set(6, i, Pawn(color="white"))

        for i, piece in enumerate(back_rank):
            self.set(0, i, piece(color="black"))
            self.set(7, i, piece(color="white"))

    def reset(self) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = None

    def get(self, row: int, col: int) -> Optional[Piece]:
        self._validate_coords(row, col)
        return self.grid[row][col]

    def set(self, row: int, col: int, piece: Piece) -> None:
        self._validate_coords(row, col)
        self.grid[row][col] = piece

    def select(self, row: int, col: int) -> List[Coordinate]:
        self._validate_coords(row, col)
        piece = self.grid[row][col]

        if piece is None:
            return []

        return [
            (move_row, move_col)
            for move_row, move_col in piece.moves((row, col), self)
            if self.in_bounds(move_row, move_col)
        ]

    def is_empty(self, row: int, col: int) -> bool:
        self._validate_coords(row, col)
        return self.grid[row][col] is None

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def _validate_coords(self, row: int, col: int) -> None:
        if not self.in_bounds(row, col):
            raise IndexError(f"Out of bounds: ({row}, {col})")

    def __str__(self) -> str:
        rows = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                piece = self.grid[r][c]

                if piece is None:
                    row.append(".")
                else:
                    row.append(piece.symbol)

            rows.append(" ".join(row))

        return "\n".join(rows)
