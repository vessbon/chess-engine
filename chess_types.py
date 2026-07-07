from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal

type Coordinate = tuple[int, int]
type CastlingSide = Literal["kingside", "queenside"]


class Color(Enum):
    WHITE = "white"
    BLACK = "black"

    @property
    def opposite(self):
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class MoveType(Enum):
    NORMAL = auto()
    CASTLE = auto()
    EN_PASSANT = auto()
    PROMOTION = auto()


@dataclass(frozen=True)
class Move:
    start: Coordinate
    end: Coordinate
    move_type: MoveType = MoveType.NORMAL


@dataclass
class CastlingRights:
    kingside: bool = True
    queenside: bool = True
