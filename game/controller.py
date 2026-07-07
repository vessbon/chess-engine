import time

from game import Game
from renderer import Renderer


class GameController:
    def __init__(self, game: Game, renderer: Renderer) -> None:
        self.game = game
        self.renderer = renderer
        self.last_frame_time = 0.0
        self.running = False

    def start_game(self) -> None:
        self.game.initialize()
        self.last_frame_time = time.perf_counter()
        self.game.state.clock.is_running = True
        self.running = True

        while self.running:
            self.update()
            time.sleep(1 / 60)

    def update(self) -> None:
        current_time = time.perf_counter()
        delta_sec = current_time - self.last_frame_time
        self.last_frame_time = current_time

        active_color = self.game.state.current_color
        self.game.state.clock.tick(active_color, delta_sec)

        if self.game.state.clock.has_flagged(active_color):
            print(f"Game Over! {active_color.opposite.value} wins on time.")
            self.running = False
            return

        print(self.game.state.clock.times)
