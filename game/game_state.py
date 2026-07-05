from dataclasses import dataclass
from typing import Literal, Optional

from chess_types import Color, Coordinate
from pieces import Piece


@dataclass
class CastlingRights:
    kingside: bool = True
    queenside: bool = True


type CastlingSide = Literal["kingside", "queenside"]


class GameState:
    def __init__(
        self,
        white_start: bool = True,
        castling_enabled: bool = True,
        start_time: float = 600_000,
    ) -> None:
        self.current_color: Color = Color.WHITE if white_start else Color.BLACK

        self.time_left: float = start_time  # ms

        self.castling: dict[Color, CastlingRights] = {
            Color.WHITE: CastlingRights(castling_enabled, castling_enabled),
            Color.BLACK: CastlingRights(),
        }

        self.white_captures: list[Piece] = []
        self.black_captures: list[Piece] = []

        self.white_points: int = 0
        self.black_points: int = 0

        self.en_passant_square: Optional[Coordinate] = None

    def toggle_moving_color(self) -> None:
        if self.current_color == Color.WHITE:
            self.current_color = Color.BLACK
        else:
            self.current_color = "white"

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
        return (
            f"{self.current_color} to move\n"
            f"{self.time_left / 1000} seconds left\n"
            f"white can{'' if self.white_castling_rights else 'not'} castle\n"
            f"black can{'' if self.black_castling_rights else 'not'} castle\n"
            f"en passant {
                'square at: ' + str(self.en_passant_square)
                if self.en_passant_square
                else 'not available'
            }\n"
            f"white points: {self.white_points}\nwhite captures: {self.white_captures}\n"
            f"black points: {self.black_points}\nblack captures: {self.black_captures}"
        )
