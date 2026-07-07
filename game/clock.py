from chess_types import Color


class ChessClock:
    def __init__(self, initial_minutes: int = 5, increment_seconds: int = 0) -> None:
        self.times = {
            Color.WHITE: float(initial_minutes * 60),
            Color.BLACK: float(initial_minutes * 60),
        }
        self.increment_sec = float(increment_seconds)
        self.is_running = False

    def tick(self, active_color: Color, delta_sec: float) -> None:
        if not self.is_running:
            return

        self.times[active_color] = max(0.0, self.times[active_color] - delta_sec)

    def commit_move(self, active_color: Color) -> None:
        if self.times[active_color] > 0:
            self.times[active_color] += self.increment_sec

    def has_flagged(self, color: Color) -> bool:
        return self.times[color] <= 0

    def get_time_string(self, color: Color) -> str:
        """Formats the internal float seconds into a clean UI string."""
        total_seconds = self.times[color]

        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        tenths = int((total_seconds % 1) * 10)

        if total_seconds < 10 and total_seconds > 0:
            return f"{seconds:02d}.{tenths}"

        return f"{minutes:02d}:{seconds:02d}"
