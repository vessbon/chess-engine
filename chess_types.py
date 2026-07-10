from dataclasses import dataclass
from enum import Enum, auto

type Coordinate = tuple[int, int]


class Color(Enum):
    WHITE = "white"
    BLACK = "black"

    @property
    def opposite(self):
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class MoveType(Enum):
    NORMAL = auto()
    CAPTURE = auto()
    CASTLE = auto()
    EN_PASSANT = auto()
    PROMOTION = auto()


class CastlingSide(Enum):
    KINGSIDE = auto()
    QUEENSIDE = auto()


class HighlightType(Enum):
    NORMAL = auto()
    CAPTURE = auto()
    LAST_MOVE = auto()
    SELECTED = auto()


@dataclass
class Highlight:
    highlight_type: HighlightType


@dataclass(frozen=True)
class Move:
    start: Coordinate
    end: Coordinate
    move_type: MoveType = MoveType.NORMAL


@dataclass
class CastlingRights:
    rights: dict[CastlingSide, bool]

    def __init__(self, castling_enabled: bool = True) -> None:
        self.rights = {
            CastlingSide.KINGSIDE: castling_enabled,
            CastlingSide.QUEENSIDE: castling_enabled,
        }

    def __getitem__(self, side: CastlingSide) -> bool:
        return self.rights[side]

    def revoke(self, side: CastlingSide) -> None:
        self.rights[side] = False
