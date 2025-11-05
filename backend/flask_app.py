from flask import Flask, request, jsonify
from flask_cors import CORS
import io, sys, builtins
from TicTacToe.TicTacToeAI import ai_move

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Flask backend for TicTacToe running successfully."

@app.route("/play", methods=["POST"])
def play_game():
    """
    Run your original ai_move() using mocked input() and captured print().
    Streamlit sends user moves as a list of strings ["0 0", "1 1", "2 2"].
    """
    moves = request.json.get("moves", [])
    captured_output = io.StringIO()

    # Backup original input and stdout
    original_input = builtins.input
    original_stdout = sys.stdout

    def fake_input(prompt=""):
        if moves:
            return moves.pop(0)
        else:
            raise EOFError

    # Redirect input and print
    builtins.input = fake_input
    sys.stdout = captured_output

    try:
        ai_move()
    except EOFError:
        # Game stopped (no moves left)
        pass
    finally:
        # Restore original state
        builtins.input = original_input
        sys.stdout = original_stdout

    # Return everything printed by your program
    output = captured_output.getvalue()
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)
