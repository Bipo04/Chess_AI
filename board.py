from const import *
from square import Square
from piece import *

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._creat()
        self._add_piece('white')
        self._add_piece('black')

    def _creat(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
        
        # tạo quân tốt
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # tạo quân mã
        self.squares[row_other][1] = Square(row_pawn, col, Knight(color))
        self.squares[row_other][6] = Square(row_pawn, col, Knight(color))

        # tạo quân tượng
        self.squares[row_other][2] = Square(row_pawn, col, Bishop(color))
        self.squares[row_other][5] = Square(row_pawn, col, Bishop(color))

        # tạo quân xe
        self.squares[row_other][0] = Square(row_pawn, col, Rook(color))
        self.squares[row_other][7] = Square(row_pawn, col, Rook(color))

        # tạo quân hậu
        self.squares[row_other][3] = Square(row_pawn, col, Queen(color))

        # tạo quân vua
        self.squares[row_other][4] = Square(row_pawn, col, King(color))