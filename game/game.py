from board import Board
from chess_types import Color, Coordinate
from pieces import King, Pawn, Rook

from .game_state import GameState


class Game:
    def __init__(self, board: Board, state: GameState) -> None:
        self.state = state
        self.board = board

    def initialize(self) -> None:
        self.board.setup()

    def legal_moves(self) -> dict[Color, dict[Coordinate, list[Coordinate]]]:
        legal_moves = {Color.WHITE: {}, Color.BLACK: {}}

        for piece, coord in self.board.get_piece_locations().items():
            row, col = coord
            legal_moves[piece.color][coord] = self.board.pseudo_moves(row, col)

        return legal_moves

    def move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> None:
        piece = self.board.get(from_row, from_col)
        if piece is None or piece.color != self.state.current_color:
            return

        target = self.board.get(to_row, to_col)
        home_row = 7 if self.state.current_color == Color.WHITE else 0

        moved = False
        castled = False

        # Castling logic
        kingside = self.state.castling[self.state.current_color].kingside
        queenside = self.state.castling[self.state.current_color].queenside

        is_castle_attempt = (
            isinstance(piece, King)
            and from_row == home_row
            and from_col == 4
            and to_row == from_row
            and to_col in (2, 6)
        )

        if is_castle_attempt:
            if to_col == 2 and queenside:
                castled = self._castle(from_row, from_col, to_col)
            elif to_col == 6 and kingside:
                castled = self._castle(from_row, from_col, to_col)
        else:
            moved = self.board.move(from_row, from_col, to_row, to_col)

        if moved or castled:
            # Castling revocation logic
            if isinstance(piece, King):
                self.state.revoke_castling(self.state.current_color, "queenside")
                self.state.revoke_castling(self.state.current_color, "kingside")

            if isinstance(piece, Rook):
                if from_col == 0:
                    self.state.revoke_castling(self.state.current_color, "queenside")
                elif from_col == 7:
                    self.state.revoke_castling(self.state.current_color, "kingside")

            # En passant logic
            self.state.clear_en_passant()
            if isinstance(piece, Pawn) and abs(to_row - from_row) == 2:
                passed_row = (from_row + to_row) // 2
                self.state.mark_en_passant((passed_row, from_col))

            # Capture logic
            if target is not None and target.color != piece.color:
                self.state.record_capture(target)

            self.next_turn()

    def _castle(self, row: int, king_from_col: int, king_to_col: int) -> bool:
        rook_from_col = 0 if king_to_col == 2 else 7
        rook_to_col = 3 if king_to_col == 2 else 5

        king = self.board.get(row, king_from_col)
        rook = self.board.get(row, rook_from_col)

        if not isinstance(king, King):
            return False

        if not isinstance(rook, Rook) or rook.color != king.color:
            return False

        path_start = min(king_from_col, rook_from_col) + 1
        path_end = max(king_from_col, rook_from_col)

        # Check if king squares are attacked
        step = 1 if king_to_col > king_from_col else -1
        for col in range(king_from_col, king_to_col + step, step):
            print(row, col)

        opposite_color_attacked_squares = {
            item
            for sublist in self.legal_moves()[king.color.opposite].values()
            for item in sublist
        }

        # Check for pieces in the way of castling
        for col in range(path_start, path_end):
            if not self.board.is_empty(row, col):
                return False

            if (row, col) in opposite_color_attacked_squares:
                return False

        self.board.set(row, king_from_col, None)
        self.board.set(row, rook_from_col, None)
        self.board.set(row, king_to_col, king)
        self.board.set(row, rook_to_col, rook)

        return True

    def next_turn(self) -> None:
        self.state.toggle_moving_color()
