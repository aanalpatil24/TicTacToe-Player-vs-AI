import sys
import os
import streamlit as st

# --- Fix import path for backend ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.game_logic import create_board, check_winner, is_draw, ai_move

# --- Page setup ---
st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")

# --- CSS Styling ---
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff !important;
        color: #000000;
    }
    .cell {
        width: 110px;
        height: 110px;
        font-size: 3rem;
        font-weight: bold;
        border: 3px solid black;     /* Black borders for visibility */
        background-color: white;     /* White cell background */
        color: black;
        text-align: center;
        vertical-align: middle;
    }
    .stButton>button {
        width: 100%;
        height: 100%;
        background: white;
        color: black;
        border: none;
        font-size: inherit;
        font-weight: inherit;
    }
    .stButton>button:hover {
        background-color: #ddd;
        cursor: pointer;
    }
    div[data-testid="stHorizontalBlock"] > div {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Title ---
st.title("🎮 Tic Tac Toe — Play vs Computer")

# --- Initialize game state ---
if "board" not in st.session_state:
    st.session_state.board = create_board()
if "winner" not in st.session_state:
    st.session_state.winner = None
if "user_symbol" not in st.session_state:
    st.session_state.user_symbol = None
if "ai_symbol" not in st.session_state:
    st.session_state.ai_symbol = None

board = st.session_state.board

# --- Step 1: Choose X or O ---
if not st.session_state.user_symbol:
    st.subheader("Choose your sign:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ (X)", use_container_width=True):
            st.session_state.user_symbol = "X"
            st.session_state.ai_symbol = "O"
            st.rerun()
    with col2:
        if st.button("⭕ (O)", use_container_width=True):
            st.session_state.user_symbol = "O"
            st.session_state.ai_symbol = "X"
            st.rerun()
else:
    user_symbol = st.session_state.user_symbol
    ai_symbol = st.session_state.ai_symbol

    st.caption(f"You are **{user_symbol}**, Computer is **{ai_symbol}**")

    # Restart game button
    if st.button("🔄 Restart Game"):
        st.session_state.board = create_board()
        st.session_state.winner = None
        st.session_state.user_symbol = None
        st.session_state.ai_symbol = None
        st.rerun()

    # --- Handle Click ---
    def handle_click(r, c):
        if board[r][c] == " " and not st.session_state.winner:
            board[r][c] = user_symbol
            if check_winner(board, user_symbol):
                st.session_state.winner = "You Win! 🏆"
                return
            if is_draw(board):
                st.session_state.winner = "It's a Draw 🤝"
                return

            # AI Move
            move = ai_move(board)
            if move:
                r_ai, c_ai = move
                board[r_ai][c_ai] = ai_symbol
                if check_winner(board, ai_symbol):
                    st.session_state.winner = "Computer Wins 💻"
                elif is_draw(board):
                    st.session_state.winner = "It's a Draw 🤝"

    # --- Display Grid ---
    for i in range(3):
        cols = st.columns(3, gap="small")
        for j in range(3):
            symbol = board[i][j]
            if symbol == "X":
                cell_text = "❌"
                color = "red"
            elif symbol == "O":
                cell_text = "⭕"
                color = "blue"
            else:
                cell_text = " "
                color = "black"

            with cols[j]:
                if not st.session_state.winner:
                    if st.button(cell_text, key=f"{i}-{j}", use_container_width=True):
                        handle_click(i, j)
                        st.rerun()
                else:
                    st.markdown(
                        f"<div class='cell' style='color:{color};'>{cell_text}</div>",
                        unsafe_allow_html=True,
                    )

    # --- Result message ---
    if st.session_state.winner:
        st.success(st.session_state.winner)
