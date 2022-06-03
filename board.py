"""Module for the internal representation of the board"""
from pieces import Pawn, Knight, Bishop, Rook, Queen, King, NoPiece, piece_to_string, string_to_piece
from models import Move

class Board:
    """Model class for the chessboard"""
    def __init__(self, fen : str = None):
        if fen is None: #if a position is not specified, set to the starting position
            self.board = [[Rook(0, 0, 'W'), Knight(0, 1, 'W'), Bishop(0, 2, 'W'), Queen(0, 3, 'W'), King(0, 4, 'W'), Bishop(0, 5, 'W'), Knight(0, 6, 'W'), Rook(0, 7, 'W')],
                          [Pawn(1, 0, 'W'), Pawn(1, 1, 'W'), Pawn(1, 2, 'W'), Pawn(1, 3, 'W'), Pawn(1, 4, 'W'), Pawn(1, 5, 'W'), Pawn(1, 6, 'W'), Pawn(1, 7, 'W')],
                          [NoPiece(2, 0, 'N'), NoPiece(2, 1, 'N'), NoPiece(2, 2, 'N'), NoPiece(2, 3, 'N'), NoPiece(2, 4, 'N'), NoPiece(2, 5, 'N'), NoPiece(2, 6, 'N'), NoPiece(2, 7, 'N')],
                          [NoPiece(3, 0, 'N'), NoPiece(3, 1, 'N'), NoPiece(3, 2, 'N'), NoPiece(3, 3, 'N'), NoPiece(3, 4, 'N'), NoPiece(3, 5, 'N'), NoPiece(3, 6, 'N'), NoPiece(3, 7, 'N')],
                          [NoPiece(4, 0, 'N'), NoPiece(4, 1, 'N'), NoPiece(4, 2, 'N'), NoPiece(4, 3, 'N'), NoPiece(4, 4, 'N'), NoPiece(4, 5, 'N'), NoPiece(4, 6, 'N'), NoPiece(4, 7, 'N')],
                          [NoPiece(5, 0, 'N'), NoPiece(5, 1, 'N'), NoPiece(5, 2, 'N'), NoPiece(5, 3, 'N'), NoPiece(5, 4, 'N'), NoPiece(5, 5, 'N'), NoPiece(5, 6, 'N'), NoPiece(5, 7, 'N')],
                          [Pawn(6, 0, 'B'), Pawn(6, 1, 'B'), Pawn(6, 2, 'B'), Pawn(6, 3, 'B'), Pawn(6, 4, 'B'), Pawn(6, 5, 'B'), Pawn(6, 6, 'B'), Pawn(6, 7, 'B')],
                          [Rook(7, 0, 'B'), Knight(7, 1, 'B'), Bishop(7, 2, 'B'), Queen(7, 3, 'B'), King(7, 4, 'B'), Bishop(7, 5, 'B'), Knight(7, 6, 'B'), Rook(7, 7, 'B')]
                        ]
        else: #if a FEN is provided, set the board to it
            self.fen_to_board(fen)

    def make_move(self, move : Move):
        """Make a move on the board"""
        try:
            self.board[move.endsquare.rank][move.endsquare.file] = self.board[move.startsquare.rank][move.startsquare.file]
            self.board[move.endsquare.rank][move.endsquare.file].square = move.endsquare
            self.board[move.startsquare.rank][move.startsquare.file] = NoPiece(move.startsquare.rank, move.startsquare.file, 'N')
        except IndexError: #moves can also be logically invalid, but this is checked at move generation
            print("Invalid move")

    def is_legal_move(self, move : Move, color : str) -> bool:
        """Check if the given move is legal (ie, does not leave the king in check)"""
        self.make_move(move)
        if not self.is_in_check(color):
            self.make_move(Move(move.endsquare, move.startsquare)) #restore the board
            return True
        else:
            self.make_move(Move(move.endsquare, move.startsquare)) #restore the board
            return False

    def is_in_check(self, color : str) -> bool:
        """Check if the given color is in check"""

        #locate king
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king = piece

        #check if any enemy pieces can attack the king
        for row in self.board:
            for piece in row:
                if piece.color != 'N' and piece.color != color:
                    for move in piece.generate_moves(self.board_to_characters()):
                        if move.endsquare == king.square:
                            return True
        return False

    def is_in_checkmate(self, color : str) -> bool:
        """Check if the given color is in checkmate"""
        if self.is_in_check(color):
            for row in self.board:
                for piece in row:
                    if piece.color == color:
                        for move in piece.generate_moves(self.board_to_characters()):
                            if self.is_legal_move(move, color):
                                return False
            return True
        else:
            return False

    def is_in_stalemate(self, color : str) -> bool:
        """Check if the given color is in stalemate"""
        if not self.is_in_check(color):
            for row in self.board:
                for piece in row:
                    if piece.color == color:
                        for move in piece.generate_moves(self.board_to_characters()):
                            if self.is_legal_move(move, color):
                                return False
            return True
        else:
            return False

    def board_to_characters(self):
        """Board as an array of strings"""
        board = [['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-']]
        rank_num = 0
        file_num = 0
        for row in self.board:
            for piece in row:
                board[rank_num][file_num] = piece_to_string(piece)
                file_num += 1
            file_num = 0
            rank_num += 1
        return board

    def board_to_fen(self):
        """Board as standard FEN notation"""
        fen = ""
        counter = 0 #number of pieces in a row
        board_as_characters = reversed(self.board_to_characters()) #to fit with chess coordinates, the board is stored in reverseg
        for row in board_as_characters:
            for piece in row:
                if piece == '-':
                    counter += 1
                else:
                    if counter != 0:
                        fen += str(counter)
                        counter = 0
                    fen += piece
            if counter != 0:
                fen += str(counter)
                counter = 0
            fen += '/'
        return fen

    def fen_to_board(self, fen : str):
        """Set a position using standard FEN notation"""
        self.board = [[NoPiece(0, 0, 'N'), NoPiece(0, 1, 'N'), NoPiece(0, 2, 'N'), NoPiece(0, 3, 'N'), NoPiece(0, 4, 'N'), NoPiece(0, 5, 'N'), NoPiece(0, 6, 'N'), NoPiece(0, 7, 'N')],
                      [NoPiece(1, 0, 'N'), NoPiece(1, 1, 'N'), NoPiece(1, 2, 'N'), NoPiece(1, 3, 'N'), NoPiece(1, 4, 'N'), NoPiece(1, 5, 'N'), NoPiece(1, 6, 'N'), NoPiece(1, 7, 'N')],
                      [NoPiece(2, 0, 'N'), NoPiece(2, 1, 'N'), NoPiece(2, 2, 'N'), NoPiece(2, 3, 'N'), NoPiece(2, 4, 'N'), NoPiece(2, 5, 'N'), NoPiece(2, 6, 'N'), NoPiece(2, 7, 'N')],
                      [NoPiece(3, 0, 'N'), NoPiece(3, 1, 'N'), NoPiece(3, 2, 'N'), NoPiece(3, 3, 'N'), NoPiece(3, 4, 'N'), NoPiece(3, 5, 'N'), NoPiece(3, 6, 'N'), NoPiece(3, 7, 'N')],
                      [NoPiece(4, 0, 'N'), NoPiece(4, 1, 'N'), NoPiece(4, 2, 'N'), NoPiece(4, 3, 'N'), NoPiece(4, 4, 'N'), NoPiece(4, 5, 'N'), NoPiece(4, 6, 'N'), NoPiece(4, 7, 'N')],
                      [NoPiece(5, 0, 'N'), NoPiece(5, 1, 'N'), NoPiece(5, 2, 'N'), NoPiece(5, 3, 'N'), NoPiece(5, 4, 'N'), NoPiece(5, 5, 'N'), NoPiece(5, 6, 'N'), NoPiece(5, 7, 'N')],
                      [NoPiece(6, 0, 'N'), NoPiece(6, 1, 'N'), NoPiece(6, 2, 'N'), NoPiece(6, 3, 'N'), NoPiece(6, 4, 'N'), NoPiece(6, 5, 'N'), NoPiece(6, 6, 'N'), NoPiece(6, 7, 'N')],
                      [NoPiece(7, 0, 'N'), NoPiece(7, 1, 'N'), NoPiece(7, 2, 'N'), NoPiece(7, 3, 'N'), NoPiece(7, 4, 'N'), NoPiece(7, 5, 'N'), NoPiece(7, 6, 'N'), NoPiece(7, 7, 'N')],
                    ]
        rank_num = 7 #reverse, to fit with chess coordinates
        file_num = 0
        for char in fen:
            if char == '/':
                rank_num -= 1
                file_num = 0
            elif char.isdigit():
                file_num += int(char)
            else:
                try:
                    self.board[rank_num][file_num] = string_to_piece(char, rank_num, file_num)
                    file_num += 1
                except IndexError:
                    print("Invalid FEN")
                    return
