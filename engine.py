"""Module for the chess engine"""
import json
import random
import copy
from board import Board
from models import Move, Square

class Engine:
    """Chess engine"""
    def __init__(self, board : Board, color : str, depth : int = 3):
        self.board = board
        self.color = color
        self.depth = depth
        self.is_in_opening = True

    def make_move(self) -> bool:
        """Engine makes a move"""

        #First check opening database
        if self.is_in_opening:
            if self.color == 'W':
                with open('openings/openings_w.json', 'r') as f:
                    opening_database = json.load(f)
                    try:
                        move_chosen = random.choice(opening_database[self.board.board_to_fen()])
                        move = Move(Square(move_chosen[0], move_chosen[1]), Square(move_chosen[2], move_chosen[3]))
                        self.board.make_move(move)
                        return True
                    except KeyError:
                        self.is_in_opening = False
            elif self.color == 'B':
                with open('openings/openings_b.json', 'r') as f:
                    opening_database = json.load(f)
                    try:
                        move_chosen = random.choice(opening_database[self.board.board_to_fen()])
                        move = Move(Square(move_chosen[0], move_chosen[1]), Square(move_chosen[2], move_chosen[3]))
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
        """Evaluate the position in terms of material, with respect to the engine's color"""
        evaluation = 0
        for row in self.board.board:
            for piece in row:
                evaluation += piece.get_value()
        if self.color == 'W':
            return evaluation
        elif self.color == 'B':
            return -evaluation

    def best_move(self, movelist : list[Move]) -> Move:
        """Engine makes the best move"""
        return self.highest_gain_move(movelist)

    def highest_gain_move(self, movelist : list[Move]) -> Move:
        """Engine makes the move with the highest material gain"""
        print(self.board.board_to_characters())
        highest_gain = self.evaluate_material()
        highest_gain_move = random.choice(movelist)
        for move in movelist:
            restore_piece = copy.deepcopy(self.board.board[move.endsquare.rank][move.endsquare.file])
            self.board.make_move(move)
            if self.evaluate_material() > highest_gain:
                highest_gain = self.evaluate_material()
                highest_gain_move = move
            self.board.make_move(Move(move.endsquare, move.startsquare))
            self.board.board[move.endsquare.rank][move.endsquare.file] = restore_piece
        return highest_gain_move
