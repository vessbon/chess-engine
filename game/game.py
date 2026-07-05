from .game_state import GameState


class Game:
    def __init__(self, state: GameState) -> None:
        self.state = state
