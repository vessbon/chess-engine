from board import Board
from game import Game, GameController, GameState
from renderer import Renderer


def main():
    board = Board()
    game_state = GameState()

    game = Game(board, game_state)
    renderer = Renderer()

    controller = GameController(game, renderer)

    controller.start_game()


if __name__ == "__main__":
    main()
