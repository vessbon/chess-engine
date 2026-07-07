from board import Board
from chess_types import CastlingSide, Color, Coordinate, Move, MoveType
from constants import (
    BLACK_HOME_ROW,
    KING_START_COL,
    KINGSIDE_KING_DEST,
    KINGSIDE_ROOK_COL,
    QUEENSIDE_KING_DEST,
    QUEENSIDE_ROOK_COL,
    ROOK_KINGSIDE_DEST,
    ROOK_QUEENSIDE_DEST,
    WHITE_HOME_ROW,
)
from pieces import King, Pawn, Piece, Rook

from .game_state import GameState


class Game:
    def __init__(self, board: Board, state: GameState) -> None:
        self.state = state
        self.board = board

    def initialize(self) -> None:
        self.board.setup()

    def legal_moves_from_square(self, row: int, col: int) -> set[Move]:
        piece = self.board.get(row, col)
        if piece is None:
            return set()

        moves = self.board.pseudo_moves(row, col)

        if isinstance(piece, Pawn):
            en_passant_move = self._en_passant_move(row, col)
            if en_passant_move:
                moves.add(en_passant_move)

        if isinstance(piece, King):
            moves.update(self._castling_moves(piece.color))

        return moves

    def legal_moves(self) -> dict[Color, set[Move]]:
        legal_moves: dict[Color, set[Move]] = {Color.WHITE: set(), Color.BLACK: set()}

        for piece, coord in self.board.get_piece_locations().items():
            row, col = coord
            legal_moves[piece.color].update(self.legal_moves_from_square(row, col))

        return legal_moves

    def attacked_squares(self, by_color: Color) -> set[Coordinate]:
        attacked: set[Coordinate] = set()

        for piece, coord in self.board.get_piece_locations().items():
            if piece.color != by_color:
                continue

            row, col = coord

            if isinstance(piece, Pawn):
                direction = -1 if piece.color == Color.WHITE else 1
                for dc in (-1, 1):
                    square = (row + direction, col + dc)
                    if self.board.in_bounds(*square):
                        attacked.add(square)
                continue

            attacked.update(piece.moves(coord, self.board))

        return attacked

    def move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> None:
        piece = self.board.get(from_row, from_col)
        if piece is None or piece.color != self.state.current_color:
            return

        legal_moves = self.legal_moves_from_square(from_row, from_col)
        matched_move = self._get_matched_move((to_row, to_col), legal_moves)
        if matched_move is None:
            return

        success, captured = self._execute_move(matched_move)

        if success:
            self._update_castling_rights(piece, from_col)
            self._update_en_passant_state(piece, from_col, from_row, to_row)

            # Capture logic
            if captured is not None and captured.color != piece.color:
                self.state.record_capture(captured)

            self.next_turn()

    def _execute_move(self, move: Move) -> tuple[bool, Piece | None]:
        success = False
        captured_piece = self.board.get(*move.end)

        if move.move_type == MoveType.CASTLE:
            success = self._castle(move.start[0], move.end[1])
        elif move.move_type == MoveType.EN_PASSANT:
            captured_piece = self.board.get(move.start[0], move.end[1])
            success = self._perform_en_passant(move)
        else:
            success = self.board.move(*move.start, *move.end)

        return (success, captured_piece)

    def _filter_checks(self, moves: list[Coordinate]):
        return moves

    def _update_en_passant_state(
        self, piece: Piece, from_col: int, from_row: int, to_row: int
    ) -> None:
        self.state.clear_en_passant()
        if isinstance(piece, Pawn) and abs(to_row - from_row) == 2:
            passed_row = (from_row + to_row) // 2
            self.state.mark_en_passant((passed_row, from_col))

    def _en_passant_move(self, row: int, col: int) -> Move | None:
        pawn = self.board.get(row, col)
        if self.state.en_passant_square is None or not isinstance(pawn, Pawn):
            return

        en_passant_row, en_passant_col = self.state.en_passant_square
        direction = 1 if pawn.color == Color.BLACK else -1

        if en_passant_row != row + direction:
            return

        if abs(en_passant_col - col) != 1:
            return

        captured = self.board.get(row, en_passant_col)
        if not isinstance(captured, Pawn) or captured.color == pawn.color:
            return

        return Move((row, col), self.state.en_passant_square, MoveType.EN_PASSANT)

    def _perform_en_passant(self, move: Move) -> bool:
        pawn = self.board.get(*move.start)
        if not isinstance(pawn, Pawn):
            return False

        en_passant_move = self._en_passant_move(*move.start)
        if not en_passant_move or move.end != en_passant_move.end:
            return False

        self.board.set(move.start[0], move.end[1], None)
        self.board.move(*move.start, *move.end)

        return True

    def _update_castling_rights(self, piece: Piece, from_col: int) -> None:
        if isinstance(piece, King):
            self.state.revoke_castling(self.state.current_color, CastlingSide.QUEENSIDE)
            self.state.revoke_castling(self.state.current_color, CastlingSide.KINGSIDE)

        if isinstance(piece, Rook):
            if from_col == QUEENSIDE_ROOK_COL:
                self.state.revoke_castling(
                    self.state.current_color, CastlingSide.QUEENSIDE
                )
            elif from_col == KINGSIDE_ROOK_COL:
                self.state.revoke_castling(
                    self.state.current_color, CastlingSide.KINGSIDE
                )

    def _castling_moves(self, color: Color) -> set[Move]:
        moves = set()
        home_row = WHITE_HOME_ROW if color == Color.WHITE else BLACK_HOME_ROW

        sides = {
            CastlingSide.KINGSIDE: {
                "rook_from": KINGSIDE_ROOK_COL,
                "king_to": KINGSIDE_KING_DEST,
            },
            CastlingSide.QUEENSIDE: {
                "rook_from": QUEENSIDE_ROOK_COL,
                "king_to": QUEENSIDE_KING_DEST,
            },
        }

        king = self.board.get(home_row, KING_START_COL)

        if not isinstance(king, King) or king.color != color:
            return moves

        opposite_color_attacked_squares = self.attacked_squares(color.opposite)

        for side, info in sides.items():
            if not self.state.castling[color][side]:
                continue

            rook = self.board.get(home_row, info["rook_from"])

            if not isinstance(rook, Rook) or rook.color != color:
                continue

            path_start = min(KING_START_COL, info["rook_from"]) + 1
            path_end = max(KING_START_COL, info["rook_from"])

            if any(
                not self.board.is_empty(home_row, col)
                for col in range(path_start, path_end)
            ):
                continue

            step = 1 if info["king_to"] > KING_START_COL else -1
            king_path = range(KING_START_COL, info["king_to"] + step, step)

            if any(
                (home_row, col) in opposite_color_attacked_squares for col in king_path
            ):
                continue

            moves.add(
                Move(
                    (home_row, KING_START_COL),
                    (home_row, info["king_to"]),
                    MoveType.CASTLE,
                )
            )

        return moves

    def _castle(self, row: int, king_to_col: int) -> bool:
        rook_from_col = (
            QUEENSIDE_ROOK_COL
            if king_to_col == QUEENSIDE_KING_DEST
            else KINGSIDE_ROOK_COL
        )

        rook_to_col = (
            ROOK_QUEENSIDE_DEST
            if king_to_col == QUEENSIDE_KING_DEST
            else ROOK_KINGSIDE_DEST
        )

        king = self.board.get(row, KING_START_COL)

        if not isinstance(king, King) or king.color != self.state.current_color:
            return False

        matched_move = self._get_matched_move(
            (row, king_to_col), self._castling_moves(king.color)
        )
        if matched_move is None:
            return False

        self.board.move(row, KING_START_COL, row, king_to_col)
        self.board.move(row, rook_from_col, row, rook_to_col)

        return True

    def _get_matched_move(
        self, to_coord: Coordinate, move_set: set[Move]
    ) -> Move | None:
        return next((m for m in move_set if m.end == to_coord), None)

    def next_turn(self) -> None:
        self.state.toggle_moving_color()
