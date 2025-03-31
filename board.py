from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._creat()
        self._add_piece('white')
        self._add_piece('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # cập nhật vị trí quân cờ
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # đánh dấu đã di chuyển
        piece.moved = True

        # xóa các bước có thể đi ở vị trí cũ
        piece.clear_moves()

        # lưu vị trí cũ
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):

        def pawn_moves():
            # đi thẳng = 2 nếu là first move 
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            
            # ăn chéo
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            # quân mã có 8 nước đi
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final  = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final  = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)
                        
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else: break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), 
                (row-1, col+1), 
                (row+0, col+1),
                (row+1, col+1), 
                (row+1, col+0), 
                (row+1, col-1), 
                (row+0, col-1), 
                (row-1, col-1)
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)
                

        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])

        elif isinstance(piece, King): 
            king_moves()

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