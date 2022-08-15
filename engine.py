"""Module for the chess engine"""
import random
import copy
from board import Board
from models import Move, Square

class Engine:
    """Chess engine"""
    def __init__(self, board : Board, color : str, depth : int = 3):
        self.board = board
        self.color = color
        self.enemy_color = 'W' if self.color == 'B' else 'B'

    def make_move(self) -> bool:
        """Engine makes a move"""
        
        best_move = self.best_move()
        if best_move:
            print(f"Engine selects the move {best_move.startsquare.rank},{best_move.startsquare.file} to {best_move.endsquare.rank},{best_move.endsquare.file}")
            self.board.make_move(best_move)
            return True
        else:
            return False

    def evaluate_material(self, color) -> int:
        """Evaluate the position in terms of material"""
        evaluation = 0
        for row in self.board.board:
            for piece in row:
                evaluation += piece.get_value()
        if color == 'W':
            return evaluation
        elif color == 'B':
            return -evaluation

    def highest_gain_move(self, movelist : list[Move], color) -> Move:
        """Returns the move with the highest material gain"""
        highest_gain = self.evaluate_material(color)
        highest_gain_move = random.choice(movelist)
        for move in movelist:
            restore_piece = copy.deepcopy(self.board.board[move.endsquare.rank][move.endsquare.file])
            self.board.make_move(move)
            if self.evaluate_material(color) >= highest_gain:
                highest_gain = self.evaluate_material(color)
                highest_gain_move = move
            self.board.make_move(Move(move.endsquare, move.startsquare))
            self.board.board[move.endsquare.rank][move.endsquare.file] = restore_piece
        return highest_gain_move

    def best_move(self) -> Move:
        """Engine recursively determines a strong move"""
        savestate = self.board.board_to_fen() #save the board
        initial_evaluation = self.evaluate_material(self.color)

        movelist : list[Move] = [] #determine all legal moves
        for row in self.board.board:
            for piece in row:
                if piece.color == self.color:
                    for move in piece.generate_moves(self.board.board_to_characters()):
                        if self.board.is_legal_move(move, self.color):
                            movelist.append(move)

        best_move = self.highest_gain_move(movelist, self.color) #returns the move with the highest material gain, if does not incur a costly immediate response
        self.board.make_move(best_move)
        enemy_movelist : list[Move] = []
        for row in self.board.board:
            for piece in row:
                if piece.color == self.enemy_color:
                    for move in piece.generate_moves(self.board.board_to_characters()):
                        if self.board.is_legal_move(move, self.enemy_color):
                            enemy_movelist.append(move)
        self.board.make_move(self.highest_gain_move(enemy_movelist, self.enemy_color))
        if self.evaluate_material(self.color) > initial_evaluation: #returns it if too much material is not lost in response
            self.board.fen_to_board(savestate) #restore the board
            return best_move


        best_move = random.choice(movelist) #makes the best defensive move
        best_evaluation = initial_evaluation
        self.board.fen_to_board(savestate) #restore the board
        for move in movelist: #test the risk every move possible creates, pick one with the lowest
            self.board.make_move(move)
            enemy_movelist : list[Move] = []
            for row in self.board.board:
                for piece in row:
                    if piece.color == self.enemy_color:
                        for enemy_move in piece.generate_moves(self.board.board_to_characters()):
                            if self.board.is_legal_move(enemy_move, self.enemy_color):
                                enemy_movelist.append(enemy_move)
            self.board.make_move(self.highest_gain_move(enemy_movelist, self.enemy_color))
            if self.evaluate_material(self.color) > best_evaluation: #pick a move that is not detrimental
                best_evaluation = self.evaluate_material(self.color)
                best_move = move
            self.board.fen_to_board(savestate) #restore the board
        return best_move
        



