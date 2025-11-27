# app.py
import streamlit as st
from typing import List, Optional
import random

st.set_page_config(page_title="Tic Tac Toe", page_icon="🎯", layout="centered")

st.title("Tic Tac Toe — Single file Streamlit app 🎯")
st.write("Play human vs human or human vs AI (unbeatable).")

# ---------- Helpers: game logic ----------
def empty_board() -> List[str]:
    return [""] * 9

def check_winner(board: List[str]) -> Optional[str]:
    wins = [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # cols
        (0,4,8), (2,4,6)            # diagonals
    ]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Tie"
    return None

def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == ""]

# Unbeatable AI: minimax
def minimax(board: List[str], player: str, ai_mark: str, human_mark: str) -> int:
    """Return score for board from AI perspective. ai_mark maximizes."""
    winner = check_winner(board)
    if winner == ai_mark:
        return 1
    if winner == human_mark:
        return -1
    if winner == "Tie":
        return 0

    moves = available_moves(board)
    if player == ai_mark:
        best = -999
        for m in moves:
            board[m] = ai_mark
            score = minimax(board, human_mark, ai_mark, human_mark)
            board[m] = ""
            best = max(best, score)
        return best
    else:
        best = 999
        for m in moves:
            board[m] = human_mark
            score = minimax(board, ai_mark, ai_mark, human_mark)
            board[m] = ""
            best = min(best, score)
        return best

def best_move(board: List[str], ai_mark: str, human_mark: str) -> int:
    moves = available_moves(board)
    best_score = -999
    best_m = random.choice(moves) if moves else -1
    for m in moves:
        board[m] = ai_mark
        score = minimax(board, human_mark, ai_mark, human_mark)
        board[m] = ""
        if score > best_score:
            best_score = score
            best_m = m
    return best_m

# ---------- Session state ----------
if "board" not in st.session_state:
    st.session_state.board = empty_board()
if "turn" not in st.session_state:
    st.session_state.turn = "X"  # X starts
if "mode" not in st.session_state:
    st.session_state.mode = "H vs H"
if "ai_mark" not in st.session_state:
    st.session_state.ai_mark = "O"
if "human_mark" not in st.session_state:
    st.session_state.human_mark = "X"
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "message" not in st.session_state:
    st.session_state.message = ""

# ---------- Controls ----------
col1, col2 = st.columns([2,1])

with col1:
    mode = st.selectbox("Mode", ["H vs H", "H vs AI (you = X)", "H vs AI (you = O)"])
with col2:
    if st.button("Reset"):
        st.session_state.board = empty_board()
        st.session_state.turn = "X"
        st.session_state.game_over = False
        st.session_state.message = ""

# apply mode
st.session_state.mode = mode
if mode == "H vs AI (you = X)":
    st.session_state.human_mark = "X"
    st.session_state.ai_mark = "O"
elif mode == "H vs AI (you = O)":
    st.session_state.human_mark = "O"
    st.session_state.ai_mark = "X"
else:
    st.session_state.human_mark = "X"
    st.session_state.ai_mark = "O"

# If human chooses to be O, AI starts as X
if mode == "H vs AI (you = O)" and not st.session_state.game_over and st.session_state.turn == st.session_state.ai_mark:
    # AI first move (random center/corner preference)
    if st.session_state.board == empty_board():
        # prefer center
        if st.session_state.board[4] == "":
            st.session_state.board[4] = st.session_state.ai_mark
        else:
            st.session_state.board[random.choice([0,2,6,8])] = st.session_state.ai_mark
        st.session_state.turn = st.session_state.human_mark

# ---------- Game grid ----------
board = st.session_state.board

def button_click(idx: int):
    if st.session_state.game_over:
        return
    if board[idx] != "":
        return
    # human move
    board[idx] = st.session_state.turn
    winner = check_winner(board)
    if winner:
        st.session_state.game_over = True
        if winner == "Tie":
            st.session_state.message = "It's a tie!"
        else:
            st.session_state.message = f"🎉 {winner} wins!"
        return
    # switch turn
    st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

    # AI move if applicable
    if st.session_state.mode != "H vs H" and st.session_state.turn == st.session_state.ai_mark and not st.session_state.game_over:
        ai_idx = best_move(board, st.session_state.ai_mark, st.session_state.human_mark)
        if ai_idx != -1:
            board[ai_idx] = st.session_state.ai_mark
        winner = check_winner(board)
        if winner:
            st.session_state.game_over = True
            if winner == "Tie":
                st.session_state.message = "It's a tie!"
            else:
                st.session_state.message = f"🎉 {winner} wins!"
            return
        st.session_state.turn = st.session_state.human_mark

# render 3x3 buttons
grid_cols = st.columns(3)
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row*3 + col
        label = board[idx] if board[idx] != "" else " "
        # create a wide button by using markdown + button
        if cols[col].button(label, key=f"btn_{idx}", help=f"Cell {idx+1}"):
            button_click(idx)

# ---------- Status ----------
st.write("---")
if st.session_state.message:
    st.success(st.session_state.message)
else:
    st.info(f"Turn: {st.session_state.turn}")

# show board matrix for debugging / clarity
with st.expander("Board (debug)"):
    st.write(board)

# Offer restart when game is over
if st.session_state.game_over:
    if st.button("Play again"):
        st.session_state.board = empty_board()
        st.session_state.turn = "X"
        st.session_state.game_over = False
        st.session_state.message = ""
        st.experimental_rerun()

st.write("")
st.markdown("**Controls:** Reset resets immediately. `Play again` appears after a finished game.")
st.markdown("Built with ❤️ using Streamlit — single-file app, easy to deploy.")
