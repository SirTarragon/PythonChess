from enum import Enum, auto


class PieceType(Enum):
    PAWN = auto()
    ROOK = auto()
    KNIGHT = auto()
    BISHOP = auto()
    QUEEN = auto()
    KING = auto()


class GameState(Enum):
    STALEMATE = auto()
    WHITE_CHECKMATED = auto()
    BLACK_CHECKMATED = auto()
    WHITE_IN_CHECK = auto()
    BLACK_IN_CHECK = auto()
    NORMAL = auto()

