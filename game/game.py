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

    def legal_moves_from_square(self, row: int, col: int):
        piece = self.board.get(row, col)
        if piece is None:
            return []

        moves = self.board.pseudo_moves(row, col)

        if isinstance(piece, Pawn):
            moves.extend(self._en_passant_moves())

        if isinstance(piece, King):
            moves.extend(self._castling_moves(piece.color))

        return self._filter_checks(moves)

    def legal_moves(self) -> dict[Color, dict[Coordinate, list[Coordinate]]]:
        legal_moves = {Color.WHITE: {}, Color.BLACK: {}}

        for piece, coord in self.board.get_piece_locations().items():
            row, col = coord
            legal_moves[piece.color][coord] = self.legal_moves_from_square(row, col)

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

    def _perform_en_passant(self, from_row: int, from_col: int) -> bool:
        pawn = self.board.get(from_row, from_col)
        if self.state.en_passant_square is None or not isinstance(pawn, Pawn):
            return False

        en_passant_row, en_passant_col = self.state.en_passant_square

        direction = 1 if pawn.color == Color.BLACK else -1

        for dc in (1, -1):
            target_col = from_col + dc
            diagonal_step: Coordinate = (from_row + direction, target_col)
            if diagonal_step == self.state.en_passant_square:
                target = self.board.get(from_row, target_col)
                if isinstance(target, Pawn) and target.color != pawn.color:
                    self.board.set(from_row, target_col, None)
                    self.board.move(from_row, from_col, en_passant_row, en_passant_col)

                return True

        return False

    def _castling_moves(self, color: Color) -> list[Coordinate]:
        moves = []

        king_from_col = 4
        home_row = 7 if color == Color.WHITE else 0

        sides = {
            "kingside": {"rook_from": 7, "king_to": 6},
            "queenside": {"rook_from": 0, "king_to": 2},
        }

        king = self.board.get(home_row, king_from_col)

        if not isinstance(king, King) or king.color != color:
            return moves

        opposite_color_attacked_squares = self.attacked_squares(color.opposite)

        for side, info in sides.items():
            if not getattr(self.state.castling[color], side):
                continue

            rook = self.board.get(home_row, info["rook_from"])

            if not isinstance(rook, Rook) or rook.color != color:
                continue

            path_start = min(king_from_col, info["rook_from"]) + 1
            path_end = max(king_from_col, info["rook_from"])

            if any(
                not self.board.is_empty(home_row, col)
                for col in range(path_start, path_end)
            ):
                continue

            step = 1 if info["king_to"] > king_from_col else -1
            king_path = range(king_from_col, info["king_to"] + step, step)

            if any(
                (home_row, col) in opposite_color_attacked_squares for col in king_path
            ):
                continue

            moves.append((home_row, info["king_to"]))

        return moves

    def _castle(self, row: int, king_to_col: int) -> bool:
        king_from_col = 4

        rook_from_col = 0 if king_to_col == 2 else 7
        rook_to_col = 3 if king_to_col == 2 else 5

        king = self.board.get(row, king_from_col)
        if not isinstance(king, King) or king.color != self.state.current_color:
            return False

        if (row, king_to_col) not in self._castling_moves(king.color):
            return False

        self.board.move(row, king_from_col, row, king_to_col)
        self.board.move(row, rook_from_col, row, rook_to_col)

        return True

    def next_turn(self) -> None:
        self.state.toggle_moving_color()
