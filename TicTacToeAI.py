import random

def print_board(board):
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 10)

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

def ai_move():
    board = [[" "] * 3 for _ in range(3)]
    player, ai = "X", "O"

    while True:
        print_board(board)

        # Player move
        try:
            r, c = map(int, input("Enter row and column (0-2): ").split())
            if board[r][c] != " ":
                print("Spot taken! Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Enter two numbers between 0 and 2.")
            continue
        board[r][c] = player

        if check_winner(board, player):
            print_board(board)
            print("You win!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # AI move
        print("Computer's turn...")
        r, c = random.choice(get_empty_cells(board))
        board[r][c] = ai

        if check_winner(board, ai):
            print_board(board)
            print("Computer wins!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    ai_move()
