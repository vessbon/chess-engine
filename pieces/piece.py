from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from chess_types import Color, Coordinate

if TYPE_CHECKING:
    from board import Board


class Piece(ABC):
    def __init__(self, color: Color) -> None:
        self.color: Color = color

    @abstractmethod
    def symbol(self) -> str:
        pass

    @abstractmethod
    def moves(self, position: Coordinate, board: Board) -> List[Coordinate]:
        pass

    def __str__(self) -> str:
        return self.symbol()
