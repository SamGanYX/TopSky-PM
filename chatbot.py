from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
import os
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()

def load_documents():
    """Load all text files from the data directory"""
    documents = []
    # Get all .txt files from the data directory
    for file_path in glob.glob("data/*.txt"):
        with open(file_path, 'r', encoding='utf-8') as file:
            documents.append(file.read())
    return documents

def create_qa_chain():
    # Load documents
    raw_documents = load_documents()
    
    # Split documents into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    documents = text_splitter.create_documents(raw_documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Create QA chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    
    return qa_chain

def main():
    # Initialize the QA chain
    qa_chain = create_qa_chain()
    chat_history = []
    
    print("Welcome! Ask me questions about the documents. Type 'quit' to exit.")
    
    while True:
        question = input("\nYour question (Type 'quit' to exit): ")
        if question.lower() == 'quit':
            break
            
        # Get response from the chain
        result = qa_chain({"question": question, "chat_history": chat_history})
        
        # Print the answer
        print("\nAnswer:", result["answer"])
        
        # Update chat history
        chat_history.append((question, result["answer"]))

if __name__ == "__main__":
    main() 