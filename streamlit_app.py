# app_streamlit.py
import streamlit as st
import requests

# Configuration
API_URL = "http://localhost:8000/query"  # Your FastAPI endpoint

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Assistant")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": prompt},  # Adjust based on your API schema
                    timeout=60
                )
                response.raise_for_status()
                answer = response.json().get("response", "No response received")
            except requests.exceptions.RequestException as e:
                answer = f"Error connecting to API: {str(e)}"
        
        st.markdown(answer)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar with options
with st.sidebar:
    st.header("Options")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()