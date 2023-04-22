import random
import os
import copy

def main():
    #simulates 2048 game

    os.system("clear")
    print("Welcome to 2048! Use the WASD keys to move pieces across the board. Colliding pieces will merge if they are equal in value. Each time a piece is created from merging, the value of that new piece is added to your score. You win if you get a 2048 piece. You lose if all of the spaces in the board get filled and there is nothing left to merge.")

    input("Press return to continue. ")
    print()
    score = 0
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    new_piece(board)
    new_piece(board)
    draw(board, score)

    while True:
        #for each move: get direction, shift board, merge board, check for win/loss
        while True:
            direction = input("Direction (WASD to shift, X to quit): ").lower()
            if direction == "x":
                draw(board, score)
                print("You quit.")
                return
            if direction in ["w", "a", "s", "d"]:
                break
            else:
                print("Invalid direction.")
        shift(board, direction)
        score = merge(board, score, direction)

        if win(board): #simultaneous win overpowers loss
            draw(board, score)
            print("You win!")
            return
        elif lose(board)=="lose":
            draw(board, score)
            print("You lose!")
            return
        else:
            if lose(board)=="not full":
                new_piece(board)
            draw(board, score)

def draw(board, score):
    # displays board in terminal
    os.system("clear")
    print("2048")
    print("---------------------------")
    for r in range(0, 4):
        for c in range(0, 4):
            piece_value = board[r][c]
            num_digits = len(str(piece_value))
            print("[", end="")
            if piece_value==0:
                print("    ", end="")
            else:
                for s in range(4-num_digits):
                    print(" ", end="")
                print(piece_value, end="")
            print("] ", end = "")
        print()
    print("---------------------------")
    print(f"Score: {score}")
    print()
    return

def shift(board, direction):
    # shifts all pieces to one side of the board based on user's specified direction
    # e.g. one row [2][0][0][2] shifted left becomes row [2][2][0][0]
    if direction == "w" or direction == "s":
        for c in range(0,4):
            new_line = []
            for r in range(0,4):
                if board[r][c]!=0:
                    new_line.append(board[r][c])
                    board[r][c]=0
            if direction == "w":
                start = 0
            elif direction == "s":
                start=4-len(new_line)
            for p in range(0,len(new_line)):
                board[p+start][c]=new_line[p]
    if direction == "a" or direction == "d":
        for r in range(0,4):
            new_line = []
            for c in range(0,4):
                if board[r][c]!=0:
                    new_line.append(board[r][c])
                    board[r][c]=0
            if direction == "a":
                start = 0
            elif direction == "d":
                start=4-len(new_line)
            for p in range(0,len(new_line)):
                board[r][p+start]=new_line[p]
    return

def merge(board, score, direction):
    # merges adjacent pieces with equivalent values
    # e.g. one row [2][2][0][0] merged left becomes row [4][0][0][0]
    if direction=="w":
        for c in [0, 1, 2, 3]:
            for r in [0, 1, 2]:
                if board[r][c]==board[r+1][c]:
                    board[r][c]*=2
                    score+=board[r][c]
                    board[r+1][c]=0
                    shift(board, direction)
    elif direction=="s":
        for c in [0, 1, 2, 3]:
            for r in [3, 2, 1]:
                if board[r][c]==board[r-1][c]:
                    board[r][c]*=2
                    score+=board[r][c]
                    board[r-1][c]=0
                    shift(board, direction)
    elif direction=="a":
        for r in [0, 1, 2, 3]:
            for c in [0, 1, 2]:
                if board[r][c]==board[r][c+1]:
                    board[r][c]*=2
                    score+=board[r][c]
                    board[r][c+1]=0
                    shift(board, direction)
    elif direction=="d":
        for r in [0, 1, 2, 3]:
            for c in [3, 2, 1]:
                if board[r][c]==board[r][c-1]:
                    board[r][c]*=2
                    score+=board[r][c]
                    board[r][c-1]=0
                    shift(board, direction)
    return score

def new_piece(board):
    # creates new piece in open slot on board
    # 10% chance piece value = 4, 90% chance piece value = 2
    while True:
        r = random.randint(0,3)
        c = random.randint(0,3)
        if board[r][c]==0:
            piece = random.randint(0,9)
            if piece==0:
                piece = 4
            else:
                piece = 2
            board[r][c]=piece
            break
    return

def win(board):
    # user wins when any piece equals 2048
    for r in range(0,4):
        for c in range(0,4):
            if board[r][c]==2048:
                return True
    return False

def lose(board):
    # user loses when board is not mergeable in any direction
    for r in range(0, 4):
        for c in range(0, 4):
            if board[r][c]==0:
                return "not full"
    merge_dirs = ["w", "a", "s", "d"]
    for i in range(0, 4):
        merged_board = copy.deepcopy(board) #deepcopy for lists inside list
        merge(merged_board, 0, merge_dirs[i])
        if board != merged_board:
            return "full"
    return "lose"


main()