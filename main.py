from board import Board
from pieces import Pawn


def main():
    board = Board()

    board.setup()

    board.set(3, 2, Pawn(color="white"))
    print(board.select(1, 3))
    print(board.select(4, 2))

    print(f"\n{board}\n")


if __name__ == "__main__":
    main()
