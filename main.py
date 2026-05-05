import streamlit as st
import random
import pandas as pd

# --- Configuration ---
st.set_page_config(page_title="Classroom Bingo", layout="centered")

# --- SHARED DATA (The "Cloud" for your app) ---
# We use cache_resource so both you and your friend see the SAME data.
@st.cache_resource
def get_shared_state():
    return {
        "drawn_numbers": [],
        "game_id": 0
    }

shared_state = get_shared_state()

def initialize_board(size):
    """Generates a board for the individual user."""
    max_val = size * size
    nums = list(range(1, max_val + 1))
    random.shuffle(nums)
    
    # Create a square grid
    rows = [nums[i:i + size] for i in range(0, len(nums), size)]
    df = pd.DataFrame(rows).astype(object)
    
    # Set Free Space
    mid = size // 2
    df.iloc[mid, mid] = "FREE"
    
    return df

# --- User-Specific Session State ---
if 'my_board' not in st.session_state:
    st.session_state.my_board = None
    st.session_state.my_size = 5

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Game Setup")
    selected_size = st.radio("Grid Size", [5, 7], index=0)
    
    if st.button("Generate My Board"):
        st.session_state.my_board = initialize_board(selected_size)
        st.session_state.my_size = selected_size

    if st.button("🔥 RESET SERVER (New Game)"):
        shared_state["drawn_numbers"] = []
        shared_state["game_id"] += 1
        st.rerun()

# --- Main UI ---
st.title("🏫 Classroom Bingo")
st.write("Both players see the same numbers drawn!")

# Drawing Logic
if st.button("🎯 DRAW NUMBER", type="primary", use_container_width=True):
    max_possible = st.session_state.my_size * st.session_state.my_size
    possible_nums = [n for n in range(1, max_possible + 1) if n not in shared_state["drawn_numbers"]]
    
    if possible_nums:
        new_num = random.choice(possible_nums)
        shared_state["drawn_numbers"].append(new_num)
        st.rerun()
    else:
        st.error("All numbers drawn!")

# Display Latest Call
if shared_state["drawn_numbers"]:
    last_call = shared_state["drawn_numbers"][-1]
    st.markdown(f"<h1 style='text-align: center; color: red;'>{last_call}</h1>", unsafe_allow_html=True)

# Display Your Board
if st.session_state.my_board is not None:
    st.subheader("Your Unique Board")
    
    def style_cells(val):
        if val == "FREE" or val in shared_state["drawn_numbers"]:
            return 'background-color: #4CAF50; color: white; border: 2px solid white;'
        return 'background-color: #f0f2f6;'

    st.table(st.session_state.my_board.style.map(style_cells))
else:
    st.info("Click 'Generate My Board' in the sidebar to start!")

# Draw History
with st.expander("Show History"):
    st.write(shared_state["drawn_numbers"])

# Auto-refresh helper
if st.button("🔄 Sync/Refresh"):
    st.rerun()
