from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from chess_types import Color, Coordinate

if TYPE_CHECKING:
    from board import Board


class Piece(ABC):
    VALUE: ClassVar[int | float]

    def __init__(self, color: Color) -> None:
        self.color: Color = color

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if "VALUE" not in cls.__dict__:
            raise TypeError(
                f"Class {cls.__name__} must define a 'VALUE' class attribute."
            )

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @abstractmethod
    def moves(self, position: Coordinate, board: Board) -> list[Coordinate]:
        pass

    def _sliding_moves(
        self, position: Coordinate, board: Board, directions
    ) -> list[Coordinate]:
        row, col = position
        moves = []

        for dr, dc in directions:
            next_row = row + dr
            next_col = col + dc

            while board.in_bounds(next_row, next_col):
                move = (next_row, next_col)
                occupant = board.get(*move)

                if occupant and occupant.color == self.color:
                    break

                moves.append(move)

                if occupant:
                    break

                next_row += dr
                next_col += dc

        return moves

    def __str__(self) -> str:
        return self.symbol
