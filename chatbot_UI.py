import streamlit as st
import requests
import time

# Set up Streamlit page
st.set_page_config(page_title="BGO AI Chatbot", page_icon="🤖", layout="wide")

# Define API endpoint
API_URL = "http://127.0.0.1:5000/chat"

# Title
st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🤖 BGO AI Chatbot</h1>", unsafe_allow_html=True)
st.write("Chat with BGO's AI-powered assistant. Type your message below!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
with st.container():
    for role, text in st.session_state.messages:
        color = "#0056b3" if role == "user" else "#f0f0f0"
        st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:10px; margin-bottom:10px;'>{text}</div>", unsafe_allow_html=True)

# User input
user_input = st.text_input("Type your message:")

if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append(("user", user_input))

        # Send request to backend
        with st.spinner("BGO AI is thinking..."):
            response = requests.post(API_URL, json={"message": user_input})
            bot_response = response.json().get("response", "No response from API.")

        # Add bot response to chat history
        st.session_state.messages.append(("bot", bot_response))

        # Refresh page to show new messages
        st.rerun()
