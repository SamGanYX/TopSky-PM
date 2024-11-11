import streamlit as st
from chatbot import create_qa_chain

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = create_qa_chain()

def main():
    st.title("Document Q&A Chatbot")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    for question, answer in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)
    
    # Chat input
    if question := st.chat_input("Ask a question about the documents"):
        # Display user message
        with st.chat_message("user"):
            st.write(question)
            
        # Get response from chatbot
        with st.chat_message("assistant"):
            result = st.session_state.qa_chain({
                "question": question, 
                "chat_history": st.session_state.chat_history
            })
            st.write(result["answer"])
        
        # Update chat history
        st.session_state.chat_history.append((question, result["answer"]))

if __name__ == "__main__":
    main()
