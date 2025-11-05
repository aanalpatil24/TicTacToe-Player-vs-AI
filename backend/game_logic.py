import random

def create_board():
    return [[" "] * 3 for _ in range(3)]

def check_winner(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def ai_move(board, ai="O"):
    empty = get_empty_cells(board)
    if empty:
        return random.choice(empty)
    return None
