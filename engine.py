from board import Board

class Engine:
    """Chess computer"""
    def __init__(self, board : Board, color : str):
        self.board = board
        self.color = color

    def make_move(self):
        """Engine makes a move"""
        for row in self.board.board:
            for piece in row:
                if piece.color == self.color:
                    for move in piece.generate_moves(self.board.board_to_characters()):
                        if self.board.is_legal_move(move, self.color):
                            print(f"I select the move {move.startsquare.rank},{move.startsquare.file} to {move.endsquare.rank},{move.endsquare.file}")
                            self.board.make_move(move)
                            return
