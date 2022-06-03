"""Module for the chess engine"""
import json
import random
from board import Board
from models import Move, Square

class Engine:
    """Chess engine"""
    def __init__(self, board : Board, color : str):
        self.board = board
        self.color = color
        self.is_in_opening = True

    def make_move(self) -> bool:
        """Engine makes a move"""

        #First check opening database
        if self.is_in_opening:
            if self.color == 'W':
                with open('./openings/openings_w.json', 'r') as f:
                    opening_database = json.load(f)
                    try:
                        moves = opening_database[self.board.board_to_fen()]
                        move = random.choice(moves)
                        move = Move(Square(move[0], move[1]), Square(move[2], move[3])) #overwrite to proper move object
                        self.board.make_move(move)
                        return True
                    except KeyError:
                        self.is_in_opening = False
            elif self.color == 'B':
                with open('openings/openings_b.json', 'r') as f:
                    opening_database = json.load(f)
                    print(opening_database)
                    print(self.board.board_to_fen())
                    try:
                        moves = opening_database[self.board.board_to_fen()]
                        move = random.choice(moves)
                        move = Move(Square(move[0], move[1]), Square(move[2], move[3])) #overwrite to proper move object
                        self.board.make_move(move)
                        return True
                    except KeyError:
                        self.is_in_opening = False
        
        #Then consult the evaluator
        legal_moves : list[Move] = []
        for row in self.board.board:
            for piece in row:
                if piece.color == self.color:
                    for move in piece.generate_moves(self.board.board_to_characters()):
                        if self.board.is_legal_move(move, self.color):
                            legal_moves.append(move)
        if legal_moves:
            best_move = self.best_move(legal_moves)
            print(f"Engine selects the move {best_move.startsquare.rank},{best_move.startsquare.file} to {best_move.endsquare.rank},{best_move.endsquare.file}")
            self.board.make_move(best_move)
            return True
        else:
            return False

    def evaluate_material(self) -> int:
        """Evaluate the position in terms of material"""
        evaluation = 0
        for row in self.board.board:
            for piece in row:
                evaluation += piece.get_value()

    def best_move(self, movelist : list[Move]) -> Move:
        """Engine makes the best move"""
        #TODO: implement
        return movelist[0]
