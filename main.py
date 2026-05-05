import streamlit as st
import pandas as pd
import random

# --- 1. Shared Server State ---
# Shared across all users (you and your friend)
@st.cache_resource
def get_shared_game_data():
    return {"called_numbers": set()}

shared_data = get_shared_game_data()

# --- 2. App Configuration ---
st.set_page_config(page_title="Classroom Bingo", layout="centered")

# --- 3. Initialize Session State (FIX FOR YOUR ERROR) ---
if "size" not in st.session_state:
    st.session_state.size = 5  # Default size
if "my_board" not in st.session_state:
    st.session_state.my_board = None

# --- 4. Functions ---
def create_board(size):
    max_val = 25 if size == 5 else 49
    nums = list(range(1, max_val + 1))
    random.shuffle(nums)
    
    # Reshape into grid
    grid = [nums[i:i + size] for i in range(0, len(nums), size)]
    df = pd.DataFrame(grid).astype(object)
    
    # Middle Free Space
    mid = size // 2
    df.iloc[mid, mid] = "FREE"
    return df

# --- 5. Sidebar ---
with st.sidebar:
    st.header("1. Setup Board")
    # We update the session state directly via the radio button
    size_choice = st.radio("Choose Size", [5, 7], key="size_selector")
    
    if st.button("Generate My Board"):
        st.session_state.size = size_choice
        st.session_state.my_board = create_board(size_choice)
        st.rerun()
    
    st.divider()
    if st.button("⚠️ Clear All Numbers (New Game)"):
        shared_data["called_numbers"].clear()
        st.rerun()

# --- 6. Main Game ---
st.title("🤝 Peer-to-Peer Bingo")

# Now this line won't crash because 'size' was defined in step 3!
current_max = 25 if st.session_state.size == 5 else 49
st.write(f"Playing **1 to {current_max}**")

# Input Section
st.subheader("2. Call a Number")
col1, col2 = st.columns([3, 1])
with col1:
    num_input = st.number_input("Type number called:", min_value=1, 
                                max_value=current_max, 
                                key="input_box")
with col2:
    if st.button("Add Number", use_container_width=True):
        shared_data["called_numbers"].add(int(num_input))
        st.rerun()

# Display Called Numbers
st.write(f"**Numbers Called so far:** {sorted(list(shared_data['called_numbers']))}")

st.divider()

# --- 7. Display Board ---
if st.session_state.my_board is not None:
    st.subheader("3. Your Board")
    
    def highlight_match(val):
        if val == "FREE" or val in shared_data["called_numbers"]:
            return 'background-color: #ff4b4b; color: white; font-weight: bold; border: 1px solid white'
        return 'background-color: #262730; color: #FAFAFA'

    st.table(st.session_state.my_board.style.map(highlight_match))
    
    if st.button("🔄 Sync with Friend"):
        st.rerun()
else:
    st.info("Click 'Generate My Board' in the sidebar to start.")
