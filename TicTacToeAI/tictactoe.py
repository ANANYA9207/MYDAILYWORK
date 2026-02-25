import math

board = [' ' for _ in range(9)]

def print_board():
    for i in range(3):
        print(board[i*3] + " | " + board[i*3+1] + " | " + board[i*3+2])
        if i < 2:
            print("--+---+--")

def check_winner(b, player):
    win_pos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for pos in win_pos:
        if b[pos[0]] == b[pos[1]] == b[pos[2]] == player:
            return True
    return False

def is_full(b):
    return ' ' not in b

def minimax(b, depth, is_max):
    if check_winner(b, 'X'):
        return 10 - depth
    if check_winner(b, 'O'):
        return depth - 10
    if is_full(b):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'
                best = max(best, minimax(b, depth+1, False))
                b[i] = ' '
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                best = min(best, minimax(b, depth+1, True))
                b[i] = ' '
        return best

def ai_move():
    best_val = -math.inf
    best_move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            move_val = minimax(board, 0, False)
            board[i] = ' '
            if move_val > best_val:
                best_move = i
                best_val = move_val
    board[best_move] = 'X'

def human_move():
    move = int(input("Enter position (1-9): ")) - 1
    if board[move] == ' ':
        board[move] = 'O'
    else:
        print("Invalid move!")
        human_move()

def main():
    print("Tic Tac Toe: You (O) vs AI (X)")
    print_board()

    while True:
        human_move()
        print_board()
        if check_winner(board, 'O'):
            print("You win!")
            break
        if is_full(board):
            print("Draw!")
            break

        ai_move()
        print("AI Move:")
        print_board()
        if check_winner(board, 'X'):
            print("AI wins!")
            break
        if is_full(board):
            print("Draw!")
            break

main()
