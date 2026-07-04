from abc import ABC, abstractmethod
from typing import List

from chess_types import Color, Coordinate


class Piece(ABC):
    def __init__(self, color: Color) -> None:
        self.color = color

    @abstractmethod
    def symbol(self) -> str:
        pass

    @abstractmethod
    def moves(self, position: Coordinate, board) -> List[Coordinate]:
        pass

    def __str__(self) -> str:
        return self.symbol()
