"""CLI"""
from board import Board
from models import Move, Square
from engine import Engine

def main():
    board = Board()
    engine = Engine(board, 'B')
    print(board.board_to_characters())
    while True:
        print("  0 1 2 3 4 5 6 7")
        rank = 0
        for row in board.board_to_characters():
            print(f"{rank}", end=" ")
            for piece in row:
                print(piece, end=" ")
            print()
            rank += 1
        startrank = int(input("Enter the starting y coord: "))
        startfile = int(input("Enter the starting x coord: "))
        endrank = int(input("Enter the ending y coord: "))
        endfile = int(input("Enter the ending x coord: "))
        board.make_move(Move(Square(startrank, startfile), Square(endrank, endfile)))
        engine.make_move()

if __name__ == '__main__':
    main()
