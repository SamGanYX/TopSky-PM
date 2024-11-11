import json
import os
from main import chatbot

# File to store the chat history
history_file = "chat_history.json"

# Load chat history from file
def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

# Save chat history to file
def save_history(history):
    with open(history_file, 'w') as file:
        json.dump(history, file)

# Wrapper to run chatbot with saved history
def start_chat():
    history = load_history()  # Load previous history

    print("Starting chat session...")
    history = chatbot(history)  # Run chatbot with loaded history
    
    save_history(history)  # Save updated history at the end of the session

if __name__ == "__main__":
    start_chat()
