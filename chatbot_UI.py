import streamlit as st
import requests

# Set up Streamlit page
st.set_page_config(page_title="BGO AI Chatbot", page_icon="🤖", layout="wide")

# API Endpoint & Secret Key
API_URL = "https://bgo-chatbot-api.onrender.com/chat"
API_SECRET_KEY = "your_super_secret_key"

# Title
st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🤖 BGO AI Chatbot</h1>", unsafe_allow_html=True)
st.write("Chat with BGO AI's assistant. Type your message below!")

# Add link to BGO Outsourcing
st.markdown("<p style='text-align: center;'><a href='https://www.billgosling.com/' target='_blank'>BGO Outsourcing</a></p>", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
with st.container():
    for role, text in st.session_state.messages:
        color = "#0056b3" if role == "user" else "#f0f0f0"
        st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:10px; margin-bottom:10px;'>{text}</div>", unsafe_allow_html=True)

# Define the function to send messages
def send_message():
    user_input = st.session_state.input_text.strip()

    if user_input:
        st.session_state.messages.append(("user", user_input))

        with st.spinner("BGO AI is thinking..."):
            response = requests.post(
                API_URL,
                json={"message": user_input},
                headers={"Authorization": f"Bearer {API_SECRET_KEY}"}
            )
            
            if response.status_code == 200:
                bot_response = response.json().get("response", "No response from API.")
            else:
                bot_response = "Error: Unable to reach the chatbot backend."

        st.session_state.messages.append(("bot", bot_response))

    # Clear input field after sending message
    st.session_state.input_text = ""
    st.rerun()

# User input box with Enter key submission
user_input = st.text_input("Type your message and press Enter:", key="input_text", on_change=send_message)

# Send button
if st.button("Send"):
    send_message()
