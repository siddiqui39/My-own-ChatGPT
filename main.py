import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
SystemMessage,
HumanMessage,
AIMessage
)

def init():
    load_dotenv()
    # Check if OpenAI API key is set
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_SECRET")== "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
        
    # Configure Streamlit page
    st.set_page_config(page_title="Your own ChatGPT",
                       page_icon="🎯")

def main():
    init()
    # Initialize the OpenAI chat model
    chat = ChatOpenAI(temperature=0)
    # Initialize conversation history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content= "You are a helpful assistant."),
        ]

    # App header
    st.header("Your own ChatGPT🎯")
    
    # Sidebar for user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key= "user_input")

        if user_input:
            # Add user message to conversation
            st.session_state.messages.append(HumanMessage(content= user_input))
            # Generate response from the model
            with st.spinner("Thinking..."):
                response= chat(st.session_state.messages)
            # Add AI response to conversation
            st.session_state.messages.append(
                AIMessage(content = response.content))

    # Display conversation messages
    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]): # Skip system message at index 0
        if i % 2 == 0:
            # User messages
            message(msg.content, is_user= True, key= str(i) + "_user")
        else:
            # AI messages
            message(msg.content, is_user = False, key = str(i) + "_ai")

if __name__ == "__main__":
    main()
