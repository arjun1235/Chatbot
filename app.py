import streamlit as st
from src.chat_engine import ChatEngine

# Page configuration
st.set_page_config(
    page_title="ArcTech AI Helpdesk",
    page_icon="💬",
    layout="centered"
)

# Load chatbot once
@st.cache_resource
def load_bot():
    return ChatEngine()

bot = load_bot()

st.title("💬 ArcTech AI Helpdesk Assistant")
st.write("Welcome! Ask me any Tier 1 IT support question.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your IT issue here...")

if user_input:

    # Show user's message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get chatbot response
    result = bot.ask(user_input)

    if result["success"]:
        reply = (
            f"{result['answer']}\n\n"
            f"**Confidence:** {result['confidence']}"
        )
    else:
        reply = (
            "I couldn't confidently answer your question.\n\n"
            f"Support Ticket **#{result['ticket']}** has been created.\n\n"
            "An IT engineer will contact you shortly."
        )

    # Show chatbot reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)