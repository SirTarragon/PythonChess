from typing import List
try:
  from enums import PieceType as Type
except ModuleNotFoundError:
  from .enums import PieceType as Type

#some pieces need to log whether/how much they moved
#But no pieces needed to track their own location, since a piece can be instantiated without a board
#Logic validation therefore needs to be done in the game/board class

class Piece:
    def __init__(self, type: Type, color: bool = True) -> None:
        self._color = color #True if white
        self._type = type

    def is_white(self) -> bool:
        return self._color

    def get_type(self) -> Type:
        return self._type


class Pawn(Piece):
    def __init__(self, color: bool = True, moved: bool = False) -> None:
        self._moved = moved
        super().__init__(Type.PAWN, color)

    def __str__(self) -> str:
        return "O"

    def move(self) -> None:
        self._moved = True

    def get_moved(self) -> int:
        return self._moved

    #for greater legibility when debugging/printing items in iterables
    __repr__ = __str__


class Rook(Piece):
    def __init__(self, color: bool = True, moved: bool = False) -> None:
        #Non-zero is true in python
        #sticking with int instead of bool here for consistency with other moved attributes
        self._moved = moved
        super().__init__(Type.ROOK, color)

    def __str__(self) -> str:
        return "R"

    def move(self) -> None:
        self._moved = True

    def get_moved(self) -> int:
        return self._moved

    __repr__ = __str__


class Knight(Piece):
    def __init__(self, color: bool = True) -> None:
        super().__init__(Type.KNIGHT, color)

    def __str__(self) -> str:
        return "N"

    __repr__ = __str__


class Bishop(Piece):
    def __init__(self, color: bool = True) -> None:
        super().__init__(Type.BISHOP, color)

    def __str__(self) -> str:
        return "B"

    __repr__ = __str__


class Queen(Piece):
    def __init__(self, color: bool = True) -> None:
        super().__init__(Type.QUEEN, color)

    def __str__(self) -> str:
        return "Q"

    __repr__ = __str__


class King(Piece):
    def __init__(self, color: bool = True, moved: bool = False) -> None:
        self._moved = moved
        super().__init__(Type.KING, color)

    def __str__(self) -> str:
        return "K"

    def move(self) -> None:
        self._moved = True

    def get_moved(self) -> int:
        return self._moved

    __repr__ = __str__
