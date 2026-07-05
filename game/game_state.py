from chess_types import Color
from pieces import Piece


class GameState:
    def __init__(
        self,
        white_start: bool = True,
        castling_enabled: bool = True,
        start_time: float = 600_000,
    ) -> None:
        self.current_color: Color = "white" if white_start else "black"

        self.time_left = start_time  # ms

        self.white_castling_rights = castling_enabled
        self.black_castling_rights = castling_enabled

        self.white_points = 0
        self.black_points = 0

    def toggle_moving_color(self) -> None:
        if self.current_color == "white":
            self.current_color = "black"
        else:
            self.current_color = "white"

    def record_capture(self, captured_piece: Piece):
        if captured_piece.color == "white":
            self.black_points += captured_piece.VALUE
        else:
            self.white_points += captured_piece.VALUE

    def __str__(self) -> str:
        return (
            f"{self.current_color} to move\n"
            f"{self.time_left / 1000} seconds left\n"
            f"white can{'' if self.white_castling_rights else 'not'} castle\n"
            f"black can{'' if self.black_castling_rights else 'not'} castle\n"
            f"white points: {self.white_points}\nblack points: {self.black_points}"
        )
