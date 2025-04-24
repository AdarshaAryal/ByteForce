import streamlit as st
import time

# --- Inject CSS for styling ---
st.markdown(
    """
    <style>
        /* Background */
        .stApp {
            background-color: #11b67a;
            color: white;
        }

        /* Headings and markdown text */
        h1, h2, h3, h4, h5, h6, p {
            color: white;
        }

        /* Info box */
        .stAlert {
            background-color: #00572C !important;
            color: white !important;
        }

        /* Buttons */
        button[kind="primary"] {
            color: black !important;
            background-color: white !important;
        }

        /* Radio options text */
        .stRadio label {
            color: white;
        }

        /* Radio circles */
        .stRadio div[role="radiogroup"] > div {
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 5px;
        }

        /* Center countdown */
        .st-emotion-cache-1v0mbdj {
            text-align: center;
        }

        /* Logo styling */
        .logo-container {
            text-align: center;
        }
        .logo-container img {
            max-width: 200px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Display the logo at the top ---
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("streamlit_demo\logo.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Simplified Title ---
st.title("Transaction Pause 🧘‍♀️💸")

# --- Initialize state ---
if 'step' not in st.session_state:
    st.session_state.step = 'mood_before'
if 'cooldown_complete' not in st.session_state:
    st.session_state.cooldown_complete = False
if 'cooldown_seconds' not in st.session_state:
    st.session_state.cooldown_seconds = 10
if 'transaction_cancelled' not in st.session_state:
    st.session_state.transaction_cancelled = False

# --- App Info ---
st.info("This transaction was flagged as potentially harmful (e.g., gambling, impulse shopping). Let's pause briefly before proceeding.")

# --- Mood input helper ---
def mood_input(label, key):
    return st.radio(label, ['😞 Bad', '😐 Okay', '😊 Good'], horizontal=True, key=key)

# --- Step 1: Mood before transaction ---
if st.session_state.step == 'mood_before':
    st.subheader("How are you feeling right now?")
    mood_before = mood_input("Your mood:", key="mood_before_input")
    if st.button("Start Cooldown"):
        st.session_state.mood_before = mood_before
        st.session_state.step = 'cooldown'
        st.rerun()

# --- Step 2: Cooldown (blocks UI) ---
elif st.session_state.step == 'cooldown' and not st.session_state.cooldown_complete:
    st.subheader("Cooldown Timer ⏳")
    st.write("Take a moment. Breathe. Reflect.")

    with st.empty():
        for remaining in range(st.session_state.cooldown_seconds, 0, -1):
            st.markdown(f"## ⏳ {remaining} seconds remaining...")
            time.sleep(1)
        st.session_state.cooldown_complete = True
        st.session_state.step = 'mood_after'
        st.rerun()

# --- Step 3: Mood after cooldown ---
elif st.session_state.step == 'mood_after':
    st.subheader("How are you feeling now?")
    mood_after = mood_input("Your mood:", key="mood_after_input")
    st.session_state.mood_after = mood_after

    st.write("### What's next?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Continue with Transaction"):
            st.session_state.step = 'summary'
            st.session_state.transaction_cancelled = False
            st.rerun()
    with col2:
        if st.button("❌ Cancel Transaction"):
            st.session_state.step = 'summary'
            st.session_state.transaction_cancelled = True
            st.rerun()

# --- Step 4: Summary ---
elif st.session_state.step == 'summary':
    if st.session_state.transaction_cancelled:
        st.warning("You've chosen not to go through with this transaction.")
        st.write("That’s a powerful decision. If you’re feeling overwhelmed, consider talking to someone you trust or visiting a support resource.")
    else:
        st.success("You're continuing with the transaction.")

    st.write("### Your Mood Check-In:")
    st.write(f"**Before:** {st.session_state.mood_before}")
    st.write(f"**After:** {st.session_state.mood_after}")

    if st.button("Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
