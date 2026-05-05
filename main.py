import streamlit as st
import random
import pandas as pd

# --- Configuration ---
st.set_page_config(page_title="Custom Bingo", layout="wide")

def initialize_game(size):
    """Initializes the game state based on selected size."""
    # Define Column Headers
    if size == 5:
        cols = ['B', 'I', 'N', 'G', 'O']
        max_val = 75
    else:
        cols = ['B', 'I', 'N', 'G', 'O', 'X', 'Z']
        max_val = 98
    
    # Calculate step for number ranges
    step = max_val // size
    board_data = {}
    
    for i, char in enumerate(cols):
        start = (i * step) + 1
        end = (i + 1) * step + 1
        board_data[char] = random.sample(range(start, end), size)
    
    df = pd.DataFrame(board_data)
    
    # Set Free Space in the exact middle
    mid = size // 2
    df.iloc[mid, mid] = "FREE"
    
    st.session_state.board = df
    st.session_state.drawn_numbers = []
    st.session_state.all_numbers = list(range(1, max_val + 1))
    random.shuffle(st.session_state.all_numbers)
    st.session_state.current_size = size

# --- Sidebar Settings ---
with st.sidebar:
    st.header("Settings")
    board_size = st.radio("Select Board Size", [5, 7], index=0)
    
    if st.button("New Game / Reset"):
        initialize_game(board_size)
        st.rerun()

# Ensure state exists on first load
if 'board' not in st.session_state or st.session_state.get('current_size') != board_size:
    initialize_game(board_size)

# --- Functions ---
def draw_number():
    if st.session_state.all_numbers:
        new_num = st.session_state.all_numbers.pop()
        st.session_state.drawn_numbers.append(new_num)
    else:
        st.error("Game Over! All numbers drawn.")

# --- Main UI ---
st.title(f"🎰 {st.session_state.current_size}x{st.session_state.current_size} Bingo")

col_board, col_stats = st.columns([2, 1])

with col_board:
    # Styling logic
    def style_cells(val):
        if val == "FREE" or val in st.session_state.drawn_numbers:
            return 'background-color: #2E7D32; color: white; font-weight: bold; border: 1px solid white'
        return 'color: #333'

    # Display Board
    st.table(st.session_state.board.style.applymap(style_cells))

with col_stats:
    st.subheader("Controls")
    if st.button("Draw Next Number", type="primary", use_container_width=True):
        draw_number()
    
    if st.session_state.drawn_numbers:
        last_num = st.session_state.drawn_numbers[-1]
        st.metric("Last Called", f"#{last_num}")
    
    st.write("---")
    st.write(f"**Numbers Drawn ({len(st.session_state.drawn_numbers)}):**")
    # Show history in a scrolling area or text block
    st.caption(", ".join(map(str, st.session_state.drawn_numbers[::-1])))
