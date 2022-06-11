"""Classes representing all pieces on the chessboard"""
from models import Square, Move

class Piece:
    """Abstract base class for all pieces"""
    def __init__(self, rank : int, file : int, color : str):
        self.square = Square(rank, file)
        self.color = color
    def generate_moves(self, board : list[list[str]]):
        """Abstract method, requires board for relative reference"""
        yield None
    def get_value(self) -> int:
        """Abstract method, returns the material value of the piece"""
        return 0

class Pawn(Piece):
    """Models a pawn on the chessboard"""
    def generate_moves(self, board : list[list[str]]):
        """Returns all possible moves for the pawn"""

        #Color dependant values
        if self.color == 'W':
            direction = 1
            starting_rank = 1
        elif self.color == 'B':
            direction = -1
            starting_rank = 6


        #Forward moves: Check if square in front is empty, or if square two in front is empty and pawn hasn't moved
        if board[self.square.rank + direction][self.square.file] == '-':
            yield Move(self.square, Square(self.square.rank + direction, self.square.file))
            if self.square.rank == starting_rank and board[starting_rank + direction * 2][self.square.file] == '-':
                yield Move(self.square, Square(starting_rank + direction * 2, self.square.file))

        #Capture moves: Check if each diagonal is an enemy, capture is possible if it is
        try:
            if is_enemy_color(piece_to_string(self), board[self.square.rank + direction][self.square.file + 1]):
                yield Move(self.square, Square(self.square.rank + direction, self.square.file + 1))
        except IndexError:
            pass
        try:
            if is_enemy_color(piece_to_string(self), board[self.square.rank + direction][self.square.file - 1]):
                if self.square.file - 1 < 0:
                    raise IndexError
                yield Move(self.square, Square(self.square.rank + direction, self.square.file - 1))
        except IndexError:
            pass
    
    def get_value(self) -> int:
        """Returns the value of the pawn"""
        if self.color == 'W':
            return 1
        elif self.color == 'B':
            return -1

class Knight(Piece):
    """Models a knight on the chessboard"""
    def generate_moves(self, board : list[list[str]]):
        """Returns all possible moves for the knight"""

        #Range of movement: All 'L' moves
        knightmoves = [
            Move(self.square, Square(self.square.rank + 2, self.square.file + 1)),
            Move(self.square, Square(self.square.rank + 2, self.square.file - 1)),
            Move(self.square, Square(self.square.rank + 1, self.square.file + 2)),
            Move(self.square, Square(self.square.rank + 1, self.square.file - 2)),
            Move(self.square, Square(self.square.rank - 2, self.square.file + 1)),
            Move(self.square, Square(self.square.rank - 2, self.square.file - 1)),
            Move(self.square, Square(self.square.rank - 1, self.square.file + 2)),
            Move(self.square, Square(self.square.rank - 1, self.square.file - 2))
        ]

        #Filter out illegal indices
        knightmoves = filter(lambda move: \
            move.endsquare.rank < 8 and move.endsquare.rank >= 0 and move.endsquare.file < 8 and move.endsquare.file >= 0, knightmoves \
        )

        #Filter out own pieces
        knightmoves = filter(lambda move: \
            not is_same_color(piece_to_string(self), board[move.endsquare.rank][move.endsquare.file]), knightmoves \
        )

        for move in knightmoves:
            yield move

    def get_value(self) -> int:
        """Returns the value of the knight"""
        if self.color == 'W':
            return 3
        elif self.color == 'B':
            return -3

class Bishop(Piece):
    """Models a bishop on the chessboard"""
    def generate_moves(self, board : list[list[str]]):
        """Returns all possible moves for the bishop"""

        #positive positive diagonal
        for i in range(1, 8):
            if self.square.rank + i > 7 or self.square.file + i > 7:
                break
            if board[self.square.rank + i][self.square.file + i] == '-':
                yield Move(self.square, Square(self.square.rank + i, self.square.file + i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank + i][self.square.file + i]):
                    yield Move(self.square, Square(self.square.rank + i, self.square.file + i))
                break

        #negative positive diagonal
        for i in range(1, 8):
            if self.square.rank - i < 0 or self.square.file + i > 7:
                break
            if board[self.square.rank - i][self.square.file + i] == '-':
                yield Move(self.square, Square(self.square.rank - i, self.square.file + i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank - i][self.square.file + i]):
                    yield Move(self.square, Square(self.square.rank - i, self.square.file + i))
                break
        
        #positive negative diagonal
        for i in range(1, 8):
            if self.square.file - i < 0 or self.square.rank + i > 7:
                break
            if board[self.square.rank + i][self.square.file - i] == '-':
                yield Move(self.square, Square(self.square.rank + i, self.square.file - i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank + i][self.square.file - i]):
                    yield Move(self.square, Square(self.square.rank + i, self.square.file - i))
                break
        
        #negative negative diagonal
        for i in range(1, 8):
            if self.square.rank - i < 0 or self.square.file - i < 0:
                break
            if board[self.square.rank - i][self.square.file - i] == '-':
                yield Move(self.square, Square(self.square.rank - i, self.square.file - i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank - i][self.square.file - i]):
                    yield Move(self.square, Square(self.square.rank - i, self.square.file - i))
                break

    def get_value(self) -> int:
        """Returns the value of the bishop"""
        if self.color == 'W':
            return 3
        elif self.color == 'B':
            return -3

class Rook(Piece):
    """Models a rook on the chessboard"""
    def generate_moves(self, board : list[list[str]]):
        """Returns all possible moves for the rook"""

        #positive horizontal moves
        for i in range(self.square.file, 8):
            if board[self.square.rank][i] == '-':
                yield Move(self.square, Square(self.square.rank, i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank][i]):
                    yield Move(self.square, Square(self.square.rank, i))
                break
        
        #negative horizontal moves
        for i in range(self.square.file, -1, -1):
            if board[self.square.rank][i] == '-':
                yield Move(self.square, Square(self.square.rank, i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank][i]):
                    yield Move(self.square, Square(self.square.rank, i))
                break

        #positive vertical moves
        for i in range(self.square.rank, 8):
            if board[i][self.square.file] == '-':
                yield Move(self.square, Square(i, self.square.file))
            else:
                if is_enemy_color(piece_to_string(self), board[i][self.square.file]):
                    yield Move(self.square, Square(i, self.square.file))
                break
        
        #negative vertical moves
        for i in range(self.square.rank, -1, -1):
            if board[i][self.square.file] == '-':
                yield Move(self.square, Square(i, self.square.file))
            else:
                if is_enemy_color(piece_to_string(self), board[i][self.square.file]):
                    yield Move(self.square, Square(i, self.square.file))
                break

    def get_value(self) -> int:
        if self.color == 'W':
            return 5
        elif self.color == 'B':
            return -5

class Queen(Piece):
    """Models a queen on the chessboard"""
    def generate_moves(self, board : list[list[str]]):
        """Returns all possible moves for the queen"""

        #positive horizontal moves
        for i in range(self.square.file, 8):
            if board[self.square.rank][i] == '-':
                yield Move(self.square, Square(self.square.rank, i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank][i]):
                    yield Move(self.square, Square(self.square.rank, i))
                break

        #negative horizontal moves
        for i in range(self.square.file, -1, -1):
            if board[self.square.rank][i] == '-':
                yield Move(self.square, Square(self.square.rank, i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank][i]):
                    yield Move(self.square, Square(self.square.rank, i))
                break

        #positive vertical moves
        for i in range(self.square.rank, 8):
            if board[i][self.square.file] == '-':
                yield Move(self.square, Square(i, self.square.file))
            else:
                if is_enemy_color(piece_to_string(self), board[i][self.square.file]):
                    yield Move(self.square, Square(i, self.square.file))
                break

        #negative vertical moves
        for i in range(self.square.rank, -1, -1):
            if board[i][self.square.file] == '-':
                yield Move(self.square, Square(i, self.square.file))
            else:
                if is_enemy_color(piece_to_string(self), board[i][self.square.file]):
                    yield Move(self.square, Square(i, self.square.file))
                break

        #positive positive diagonal
        for i in range(1, 8):
            if self.square.rank + i > 7 or self.square.file + i > 7:
                break
            if board[self.square.rank + i][self.square.file + i] == '-':
                yield Move(self.square, Square(self.square.rank + i, self.square.file + i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank + i][self.square.file + i]):
                    yield Move(self.square, Square(self.square.rank + i, self.square.file + i))
                break

        #negative positive diagonal
        for i in range(1, 8):
            if self.square.rank - i < 0 or self.square.file + i > 7:
                break
            if board[self.square.rank - i][self.square.file + i] == '-':
                yield Move(self.square, Square(self.square.rank - i, self.square.file + i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank - i][self.square.file + i]):
                    yield Move(self.square, Square(self.square.rank - i, self.square.file + i))
                break
        
        #positive negative diagonal
        for i in range(1, 8):
            if self.square.file - i < 0 or self.square.rank + i > 7:
                break
            if board[self.square.rank + i][self.square.file - i] == '-':
                yield Move(self.square, Square(self.square.rank + i, self.square.file - i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank + i][self.square.file - i]):
                    yield Move(self.square, Square(self.square.rank + i, self.square.file - i))
                break
        
        #negative negative diagonal
        for i in range(1, 8):
            if self.square.rank - i < 0 or self.square.file - i < 0:
                break
            if board[self.square.rank - i][self.square.file - i] == '-':
                yield Move(self.square, Square(self.square.rank - i, self.square.file - i))
            else:
                if is_enemy_color(piece_to_string(self), board[self.square.rank - i][self.square.file - i]):
                    yield Move(self.square, Square(self.square.rank - i, self.square.file - i))
                break
        
        if self.color == 'W':
            return 9
        elif self.color == 'B':
            return -9

class King(Piece):
    """Models a king on the chessboard"""
    def generate_moves(self, board : list[list[str]]):
        """Returns all possible moves for the king"""

        #Range of movement: All 1 step moves
        kingmoves = [
            Move(self.square, Square(self.square.rank + 1, self.square.file)),
            Move(self.square, Square(self.square.rank - 1, self.square.file)),
            Move(self.square, Square(self.square.rank, self.square.file + 1)),
            Move(self.square, Square(self.square.rank, self.square.file - 1)),
            Move(self.square, Square(self.square.rank + 1, self.square.file + 1)),
            Move(self.square, Square(self.square.rank + 1, self.square.file - 1)),
            Move(self.square, Square(self.square.rank - 1, self.square.file + 1)),
            Move(self.square, Square(self.square.rank - 1, self.square.file - 1))
        ]

        #Filter out illegal indices
        kingmoves = filter(lambda move: \
            move.endsquare.rank < 8 and move.endsquare.rank >= 0 and move.endsquare.file < 8 and move.endsquare.file >= 0, kingmoves \
        )

        #Filter out own pieces
        kingmoves = filter(lambda move: \
            not is_same_color(piece_to_string(self), board[move.endsquare.rank][move.endsquare.file]), kingmoves \
        )

        for move in kingmoves:
            yield move
    
    def get_value(self):
        """Returns the value of the king"""
        if self.color == 'W':
            return 100
        elif self.color == 'B':
            return -100

class NoPiece(Piece):
    """Represents an empty square"""
    def generate_moves(self, board : list[list[str]]):
        """Returns no moves"""
        return []
    
    def get_value(self):
        """Returns 0"""
        return 0

def piece_to_string(piece : Piece):
    """Returns a string representation of a piece"""
    if isinstance(piece, Pawn):
        return 'P' if piece.color == 'W' else 'p'
    if isinstance(piece, Knight):
        return 'N' if piece.color == 'W' else 'n'
    if isinstance(piece, Bishop):
        return 'B' if piece.color == 'W' else 'b'
    if isinstance(piece, Rook):
        return 'R' if piece.color == 'W' else 'r'
    if isinstance(piece, Queen):
        return 'Q' if piece.color == 'W' else 'q'
    if isinstance(piece, King):
        return 'K' if piece.color == 'W' else 'k'
    else:
        return '-'

def string_to_piece(piece : str, rank : int, file : int):
    """Returns a piece object from a string representation of a piece"""
    match(piece):
        case 'P':
            return Pawn(rank, file, 'W')
        case 'p':
            return Pawn(rank, file, 'B')
        case 'N':
            return Knight(rank, file, 'W')
        case 'n':
            return Knight(rank, file, 'B')
        case 'B':
            return Bishop(rank, file, 'W')
        case 'b':
            return Bishop(rank, file, 'B')
        case 'R':
            return Rook(rank, file, 'W')
        case 'r':
            return Rook(rank, file, 'B')
        case 'Q':
            return Queen(rank, file, 'W')
        case 'q':
            return Queen(rank, file, 'B')
        case 'K':
            return King(rank, file, 'W')
        case 'k':
            return King(rank, file, 'B')
        case '-':
            return NoPiece(rank, file, 'N')

def is_same_color(piece1 : str, piece2 : str):
    """Returns true if the two character representations of a piece are of the same color"""
    return piece1.islower() and piece2.islower() or piece1.isupper() and piece2.isupper()

def is_enemy_color(piece1 : str, piece2 : str):
    """Returns true if the two character representations of a piece are of different colors"""
    return piece1.islower() and piece2.isupper() or piece1.isupper() and piece2.islower()
