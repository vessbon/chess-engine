from chess_types import CastlingRights, CastlingSide, Color, Coordinate
from pieces import Piece

from .clock import ChessClock


class GameState:
    def __init__(
        self,
        white_start: bool = True,
        castling_enabled: bool = True,
    ) -> None:
        self.current_color: Color = Color.WHITE if white_start else Color.BLACK

        self.clock = ChessClock(initial_minutes=5, increment_seconds=3)

        self.castling: dict[Color, CastlingRights] = {
            Color.WHITE: CastlingRights(castling_enabled),
            Color.BLACK: CastlingRights(castling_enabled),
        }

        self.white_captures: list[Piece] = []
        self.black_captures: list[Piece] = []

        self.white_points: int = 0
        self.black_points: int = 0

        self.en_passant_square: Coordinate | None = None

    def toggle_moving_color(self) -> None:
        if self.current_color == Color.WHITE:
            self.current_color = Color.BLACK
        else:
            self.current_color = Color.WHITE

    def mark_en_passant(self, square: Coordinate):
        self.en_passant_square = square

    def clear_en_passant(self):
        self.en_passant_square = None

    def revoke_castling(self, color: Color, side: CastlingSide) -> None:
        self.castling[color].revoke(side)

    def record_capture(self, captured_piece: Piece):
        self._give_points(self.current_color, int(captured_piece.VALUE))
        if self.current_color == Color.WHITE:
            self.white_captures.append(captured_piece)
        else:
            self.black_captures.append(captured_piece)

    def _give_points(self, color: Color, value: int):
        if color == Color.WHITE:
            self.white_points += value
        else:
            self.black_points += value

    def __str__(self) -> str:
        white_castling_rights = (
            self.castling[Color.WHITE][CastlingSide.KINGSIDE]
            or self.castling[Color.WHITE][CastlingSide.QUEENSIDE]
        )
        black_castling_rights = (
            self.castling[Color.BLACK][CastlingSide.KINGSIDE]
            or self.castling[Color.BLACK][CastlingSide.QUEENSIDE]
        )

        return (
            f"{self.current_color.value} to move\n"
            f"white time left: {self.clock.get_time_string(Color.WHITE)}\n"
            f"black time left: {self.clock.get_time_string(Color.BLACK)}\n"
            f"white can{'' if white_castling_rights else 'not'} castle\n"
            f"black can{'' if black_castling_rights else 'not'} castle\n"
            f"en passant {
                'square at: ' + str(self.en_passant_square)
                if self.en_passant_square
                else 'not available'
            }\n"
            f"white points: {self.white_points}\nwhite captures: {self.white_captures}\n"
            f"black points: {self.black_points}\nblack captures: {self.black_captures}"
        )
