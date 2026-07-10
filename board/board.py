import builtins

from chess_types import Color, Coordinate, Move, MoveType
from constants import (
    BLACK_HOME_ROW,
    BLACK_PAWN_ROW,
    BOARD_DIMENSION,
    WHITE_HOME_ROW,
    WHITE_PAWN_ROW,
)
from pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self) -> None:
        self.size = BOARD_DIMENSION
        self.grid: list[list[Piece | None]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]

    def setup(self) -> None:
        self.reset()

        back_rank: list[type[Piece]] = [
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
            self.set(BLACK_PAWN_ROW, i, Pawn(Color.BLACK))
            self.set(WHITE_PAWN_ROW, i, Pawn(Color.WHITE))

        for i, piece in enumerate(back_rank):
            self.set(BLACK_HOME_ROW, i, piece(Color.BLACK))
            self.set(WHITE_HOME_ROW, i, piece(Color.WHITE))

    def reset(self) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = None

    def get(self, row: int, col: int) -> Piece | None:
        self._validate_coords(row, col)
        return self.grid[row][col]

    def set(self, row: int, col: int, piece: Piece | None) -> None:
        self._validate_coords(row, col)
        self.grid[row][col] = piece

    def get_pieces(self) -> list[Piece]:
        return [piece for _, piece in self._iter_pieces()]

    def get_piece_locations(self) -> dict[Piece, Coordinate]:
        return {piece: coord for coord, piece in self._iter_pieces()}

    def move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        self._validate_coords(to_row, to_col)
        piece = self.get(from_row, from_col)
        if piece is None:
            return False

        self.set(from_row, from_col, None)
        self.set(to_row, to_col, piece)
        return True

    def pseudo_moves(self, row: int, col: int) -> builtins.set[Move]:
        self._validate_coords(row, col)
        piece = self.grid[row][col]

        if piece is None:
            return set()

        moves = set()

        for move_row, move_col in piece.moves((row, col), self):
            if not self.in_bounds(move_row, move_col):
                continue

            occupant = self.get(move_row, move_col)

            if isinstance(occupant, King):
                continue

            move_type = MoveType.CAPTURE if occupant is not None else MoveType.NORMAL

            moves.add(Move((row, col), (move_row, move_col), move_type))

        return moves

    def has_piece(self, row: int, col: int) -> bool:
        return self.in_bounds(row, col) and self.get(row, col) is not None

    def is_empty(self, row: int, col: int) -> bool:
        self._validate_coords(row, col)
        return self.grid[row][col] is None

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def _validate_coords(self, row: int, col: int) -> None:
        if not self.in_bounds(row, col):
            raise IndexError(f"Out of bounds: ({row}, {col})")

    def _iter_pieces(self):
        for row in range(self.size):
            for col in range(self.size):
                if (piece := self.get(row, col)) is not None:
                    yield (row, col), piece

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
