"""Representations for squares and moves on the chessboard"""

class Square:
    """Representation of a square on the chess board"""
    def __init__(self, rank : int, file : int):
        self.rank = rank
        self.file = file

class Move:
    """Models a potentional move"""
    def __init__(self, startsquare : Square, endsquare : Square):
        self.startsquare = startsquare
        self.endsquare = endsquare
