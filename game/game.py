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

        moved = self.board.move(from_row, from_col, to_row, to_col)
        if moved:
            # Castling logic
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

    def next_turn(self) -> None:
        self.state.toggle_moving_color()
