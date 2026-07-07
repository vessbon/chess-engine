from enum import Enum


class Color(Enum):
    WHITE = "white"
    BLACK = "black"

    @property
    def opposite(self):
        return Color.BLACK if self is Color.WHITE else Color.WHITE


type Coordinate = tuple[int, int]
