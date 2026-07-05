from chess_types import Color


class GameState:
    def __init__(
        self,
        white_start: bool = True,
        castling_enabled: bool = True,
        start_time: float = 600_000,
    ) -> None:
        self.white_to_move = white_start

        self.time_left = start_time  # ms

        self.white_castling_rights = castling_enabled
        self.black_castling_rights = castling_enabled

        self.white_points = 0
        self.black_points = 0

    def switch_moving_color(self) -> None:
        self.white_to_move = not self.white_to_move

    def give_points(self, color: Color, value: int) -> None:
        if color == "white":
            self.white_points += value
        else:
            self.black_points += value

    def __str__(self) -> str:
        return (
            f"{'white' if self.white_to_move else 'black'} to move\n"
            f"{self.time_left / 1000} seconds left\n"
            f"white can{'' if self.white_castling_rights else 'not'} castle\n"
            f"black can{'' if self.black_castling_rights else 'not'} castle\n"
            f"white points: {self.white_points}\nblack points: {self.black_points}"
        )
