game_over = False
from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

board = [' ' for _ in range(9)]

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

@app.route('/')
def home():
    return render_template('index.html', board=board)

@app.route('/move', methods=['POST'])
def move():
    global board, game_over
    data = request.json
    pos = data['pos']

    if game_over:
        return jsonify(board=board, status="Game over! Press Reset")

    if board[pos] == ' ':
        board[pos] = 'O'

        if not check_winner(board, 'O') and not is_full(board):
            ai_move()

    status = "playing"

    if check_winner(board, 'X'):
        status = "AI wins!"
        game_over = True
    elif check_winner(board, 'O'):
        status = "You win!"
        game_over = True
    elif is_full(board):
        status = "Draw!"
        game_over = True

    return jsonify(board=board, status=status)


@app.route('/reset')
def reset():
    global board, game_over
    board = [' ' for _ in range(9)]
    game_over = False
    return jsonify(board=board)


if __name__ == '__main__':
    app.run(debug=True)
