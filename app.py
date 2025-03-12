import streamlit as st
import random

# Apply a streamlined theme
st.set_page_config(page_title="Number Guessing Game", layout="wide")

st.markdown(
    """
    <style>
        .stApp { margin: auto; padding: 20px; }
        .stButton > button { width: 100%; border-radius: 8px; background-color: #ff6f61; color: white; font-weight: bold; padding: 12px; border: none; }
        .stButton > button:hover { background-color: #e63946; color: white !important; }
        .stNumberInput > div { width: 100%; }
        .stRadio { padding: 10px 0; }
        h1 { color: #2c3e50; text-align: center; font-weight: bold; }
        .sidebar-container { background-color: #f8f9fa; padding: 20px; border-radius: 12px; }
        .sidebar-container h2, .sidebar-container h3 { color: #1e88e5; }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables if not already set
if 'min_val' not in st.session_state:
    st.session_state.min_val = 1
if 'max_val' not in st.session_state:
    st.session_state.max_val = 100
if 'target' not in st.session_state:
    st.session_state.target = random.randint(st.session_state.min_val, st.session_state.max_val)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Easy"

# Function to reset the game
def reset_game():
    st.session_state.target = random.randint(st.session_state.min_val, st.session_state.max_val)
    st.session_state.attempts = 0
    st.session_state.feedback = ""
    set_difficulty(st.session_state.difficulty)

def set_difficulty(level):
    """
    Set the difficulty level:
    - Easy: Unlimited attempts.
    - Medium: 10 attempts.
    - Hard: 5 attempts.
    """
    st.session_state.difficulty = level
    if level == "Easy":
        st.session_state.max_attempts = None  # Unlimited attempts
    elif level == "Medium":
        st.session_state.max_attempts = 10
    elif level == "Hard":
        st.session_state.max_attempts = 5

# Streamlit UI
st.title("🎯 Number Guessing Game 🎲")

col1, col2 = st.columns([1, 2])

with col1:
    st.sidebar.header("⚙️ Game Settings")
    with st.sidebar.container():
        st.session_state.min_val = st.number_input("Minimum Value", value=1, step=1)
        st.session_state.max_val = st.number_input("Maximum Value", value=100, step=1)
    
    st.sidebar.subheader("🎮 Select Difficulty")
    st.sidebar.write("- **Easy:** Unlimited attempts")
    st.sidebar.write("- **Medium:** 10 attempts limit")
    st.sidebar.write("- **Hard:** 5 attempts limit")
    
    difficulty = st.sidebar.radio("Choose Level", ("Easy", "Medium", "Hard"), index=("Easy", "Medium", "Hard").index(st.session_state.difficulty), on_change=lambda: set_difficulty(difficulty))
    set_difficulty(difficulty)
    
    if st.sidebar.button("🔄 Start New Game"):
        reset_game()
        st.session_state.target = random.randint(st.session_state.min_val, st.session_state.max_val)

with col2:
    st.subheader(f"🔢 Guess a number from {st.session_state.min_val} to {st.session_state.max_val}")
    
    guess = st.number_input(f"🔢 Enter your guess between {st.session_state.min_val} and {st.session_state.max_val}", min_value=st.session_state.min_val, max_value=st.session_state.max_val, step=1)
    
    if st.button("✅ Submit Guess"):
        st.session_state.attempts += 1
        if guess < st.session_state.target:
            st.session_state.feedback = "🔻 Too low! Try again."
        elif guess > st.session_state.target:
            st.session_state.feedback = "🔺 Too high! Try again."
        else:
            st.session_state.feedback = f"🎉 Congratulations! You guessed the number in {st.session_state.attempts} attempts."
        
        if st.session_state.max_attempts and st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.feedback += "\n❌ Game over! You've reached the max attempts. Try again!"
            st.session_state.target = random.randint(st.session_state.min_val, st.session_state.max_val)  # Reset target
    
    st.write(st.session_state.feedback)
    st.write(f"📝 Attempts: {st.session_state.attempts} / {st.session_state.max_attempts if st.session_state.max_attempts else 'Unlimited'}")
    
    if st.button("🔄 Reset Game"):
        reset_game()
