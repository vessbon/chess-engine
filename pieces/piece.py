from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color) -> None:
        self.color = color

    @abstractmethod
    def symbol(self) -> str:
        pass

    """ @abstractmethod
    def moves(self, position, board):
        pass """

    def __str__(self) -> str:
        return self.symbol()
