import streamlit as st
import random
import pandas as pd

# --- Configuration ---
st.set_page_config(page_title="Pro Bingo", layout="wide", page_icon="🎰")

def initialize_game(size):
    """Initializes the game state based on selected size."""
    # Define Column Headers and Ranges
    if size == 5:
        cols = ['B', 'I', 'N', 'G', 'O']
        max_val = 75
    else:
        # For 7x7, we add more letters and increase the range
        cols = ['B', 'I', 'N', 'G', 'O', 'X', 'Z']
        max_val = 98
    
    # Calculate unique number ranges for each column
    step = max_val // size
    board_data = {}
    
    for i, char in enumerate(cols):
        start = (i * step) + 1
        end = (i + 1) * step + 1
        board_data[char] = random.sample(range(start, end), size)
    
    # FIX: .astype(object) prevents the TypeError when inserting "FREE"
    df = pd.DataFrame(board_data).astype(object)
    
    # Set Free Space in the exact middle
    mid = size // 2
    df.iloc[mid, mid] = "FREE"
    
    # Update Session State
    st.session_state.board = df
    st.session_state.drawn_numbers = []
    st.session_state.all_numbers = list(range(1, max_val + 1))
    random.shuffle(st.session_state.all_numbers)
    st.session_state.current_size = size

# --- Sidebar ---
with st.sidebar:
    st.header("Game Settings")
    board_size = st.radio("Choose Layout", [5, 7], index=0, help="5x5 uses numbers 1-75. 7x7 uses 1-98.")
    
    if st.button("Start New Game", type="primary", use_container_width=True):
        initialize_game(board_size)
        st.rerun()
    
    st.divider()
    st.info("The middle square is a FREE space. Numbers will turn green when they match a call!")

# --- Initialize on First Run ---
if 'board' not in st.session_state or st.session_state.get('current_size') != board_size:
    initialize_game(board_size)

# --- Game Logic ---
def draw_number():
    if st.session_state.all_numbers:
        new_num = st.session_state.all_numbers.pop()
        st.session_state.drawn_numbers.append(new_num)
    else:
        st.balloons()
        st.error("All numbers have been called!")

# --- Main Interface ---
st.title(f"🎰 {st.session_state.current_size}x{st.session_state.current_size} Bingo")

col_left, col_right = st.columns([3, 2])

with col_left:
    # Cell Styling Logic
    def style_cells(val):
        if val == "FREE" or val in st.session_state.drawn_numbers:
            return 'background-color: #2E7D32; color: white; font-weight: bold; font-size: 20px; text-align: center;'
        return 'text-align: center; font-size: 18px;'

    # Using .map for newer Pandas versions (replaces applymap)
    st.table(st.session_state.board.style.map(style_cells))

with col_right:
    st.subheader("Caller's Desk")
    
    if st.button("🎯 Draw Next Number", use_container_width=True):
        draw_number()
    
    # Display Current Number
    if st.session_state.drawn_numbers:
        current = st.session_state.drawn_numbers[-1]
        st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
                <h1 style="margin:0; color:#ff4b4b;">{current}</h1>
                <p style="margin:0; color:#555;">Latest Call</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Call History
    st.write("**Call History (Recent First):**")
    history = st.session_state.drawn_numbers[::-1]
    st.write(", ".join(map(str, history)) if history else "No numbers called yet.")

# --- Winner Check (Bonus Feature) ---
# This checks if the user clicks it, just for fun!
if st.button("Check for Bingo?"):
    st.toast("Checking your board...", icon="🔍")
    # You can expand logic here to auto-detect rows/cols/diagonals
    st.write("Keep playing until you see a line!")
