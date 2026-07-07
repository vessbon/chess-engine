from board import Board
from game import Game, GameState


def main():
    board = Board()
    game_state = GameState()

    game = Game(board, game_state)
    game.initialize()

    game.move(6, 1, 4, 1)
    game.move(1, 7, 2, 7)

    game.move(4, 1, 3, 1)
    game.move(2, 7, 3, 7)

    game.move(6, 3, 4, 3)
    game.move(3, 7, 4, 7)

    game.move(4, 3, 3, 3)
    game.move(4, 7, 5, 7)

    game.move(7, 3, 6, 3)
    game.move(1, 2, 3, 2)

    game.move(3, 3, 2, 2)

    print(f"\n{game.board}\n")
    print(f"\n{game.state}\n")


if __name__ == "__main__":
    main()
