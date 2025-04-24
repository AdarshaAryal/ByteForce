import streamlit as st
import time
from chat_api_conn import get_response  # Assuming you have a function to get chat responses

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
            background-color: #009d5c !important;
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
            width: 100px;  /* set the width */
            height: auto;  /* maintain aspect ratio */
        }

        /* Chat interface styling */
        .chat-container {
            background-color: #009d5c;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            height: 350px;
            overflow-y: scroll;
        }

        .chat-bot {
            background-color: #00864F;
            padding: 8px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .chat-user {
            background-color: #11b67a;
            padding: 8px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        /* Chat input area */
        .chat-input-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 10px;
        }

        .chat-input {
            width: 85%;
            padding: 10px;
            border-radius: 8px;
            border: none;
            background-color: #e0e0e0;
        }

        .send-button {
            background-color: #00864F;
            color: white;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            border: none;
            margin-left: 10px;
        }
        
        .send-button:hover {
            background-color: #007C42;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Display the logo at the top ---
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("streamlit_demo/logo.png")  # logo with CSS for resizing
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
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ""

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
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Continue with Transaction"):
            st.session_state.step = 'summary'
            st.session_state.transaction_cancelled = False
            st.rerun()
    with col2:
        if st.button("💬 Talk it through"):
            # Clear the screen and initiate chat
            st.session_state.chat_active = True
            st.session_state.step = 'chat'
            st.session_state.chat_history = "Bot: Hi! I'm here to help you reflect on your feelings regarding this transaction."
            
            st.rerun()
    with col3:
        if st.button("❌ Cancel Transaction"):
            st.session_state.step = 'summary'
            st.session_state.transaction_cancelled = True
            st.rerun()

# --- Step 4: Chat Interface ---
elif st.session_state.step == 'chat' and st.session_state.chat_active:
    
    st.title("Talk it through 🤖")
    chat_history = ""
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        chat_history = ""
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How are you feeling?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        chat_history += f"\n User: {prompt}"
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_response(chat_history)  # Call your chat API function here
        chat_history += f"\n Bot: {response}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "bot", "content": response})


    # # Clear all previous UI elements
    # st.empty()

    # # Chat container
    # st.subheader("Talk it through 🤖")
    # st.write("Ask me anything or tell me your feelings...")

    # # Display chat history
    # for message in st.session_state.chat_history:
    #     if message.startswith("Bot:"):
    #         st.markdown(f'<div class="chat-bot">{message}</div>', unsafe_allow_html=True)
    #     else:
    #         st.markdown(f'<div class="chat-user">{message}</div>', unsafe_allow_html=True)

    # # Input bar for new messages
    # user_input = st.text_area("Your Message", "", key="user_input", height=100)
    
    # # Send button
    # if st.button("Send", key="send_button"):
    #     if user_input:
    #         # Add the user's message to the chat history
    #         st.session_state.chat_history.append(f"You: {user_input}")
    #         st.markdown(f'<div class="chat-user">You: {user_input}</div>', unsafe_allow_html=True)

    #         # Placeholder bot response
    #         # st.session_state.chat_history.append("Bot: It seems like you might be feeling uncertain. Let’s explore that feeling.")
    #         # st.markdown(f'<div class="chat-bot">Bot: It seems like you might be feeling uncertain. Let’s explore that feeling.</div>', unsafe_allow_html=True)
    #         response = get_response(user_input)
    #         st.session_state.chat_history.append(f"Bot: {response}")
    #         st.markdown(f'<div class="chat-bot">Bot: {response}</div>', unsafe_allow_html=True)
    #     else:
    #         st.warning("Please type a message to continue.")

    # Close chat button
    if st.button("Close Chat"):
        st.session_state.chat_active = False
        st.session_state.step = 'mood_after'
        st.rerun()

# --- Step 5: Summary ---
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
