
import streamlit as st
import math

st.set_page_config(
    page_title="AI Tic-Tac-Toe",
    page_icon="🎮",
    layout="centered"
)

# Initialize the board
if "board" not in st.session_state:
    st.session_state.board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def check_draw(board):
    return (
        all(cell != " " for row in board for cell in row)
        and not check_winner(board, "X")
        and not check_winner(board, "O")
    )

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, maximizing, alpha, beta):
    if check_winner(board, "O"):
        return 10 - depth

    if check_winner(board, "X"):
        return depth - 10

    if check_draw(board):
        return 0

    if maximizing:
        best_score = -math.inf

        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"

                    score = minimax(
                        board, depth + 1, False, alpha, beta
                    )

                    board[r][c] = " "
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)

                    if beta <= alpha:
                        break

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = math.inf

        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"

                    score = minimax(
                        board, depth + 1, True, alpha, beta
                    )

                    board[r][c] = " "
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)

                    if beta <= alpha:
                        break

            if beta <= alpha:
                break

        return best_score

# Select the AI's best move
def ai_move(board):
    best_score = -math.inf
    best_move = None

    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "O"

                score = minimax(
                    board, 0, False, -math.inf, math.inf
                )

                board[r][c] = " "

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    if best_move is not None:
        r, c = best_move
        board[r][c] = "O"

def game_over(board):
    return (
        check_winner(board, "X")
        or check_winner(board, "O")
        or check_draw(board)
    )

# Web interface
st.title("🎮 AI Tic-Tac-Toe")
st.write("You are **X**. The AI is **O**.")
st.caption("Powered by Minimax and Alpha-Beta Pruning")

board = st.session_state.board

if st.button("🔄 New Game", use_container_width=True):
    st.session_state.board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    st.rerun()

st.subheader("Game Board")

for r in range(3):
    cols = st.columns(3)

    for c in range(3):
        symbol = board[r][c]
        label = symbol if symbol != " " else "·"

        if cols[c].button(
            label,
            key=f"cell_{r}_{c}",
            disabled=(symbol != " " or game_over(board)),
            use_container_width=True
        ):
            board[r][c] = "X"

            if not check_winner(board, "X") and not check_draw(board):
                ai_move(board)

            st.rerun()

# Display game result
if check_winner(board, "X"):
    st.success("🎉 Congratulations! You win!")
elif check_winner(board, "O"):
    st.error("🤖 AI wins! Try again.")
elif check_draw(board):
    st.info("It's a draw!")
else:
    st.info("Your turn! Select an empty cell.")