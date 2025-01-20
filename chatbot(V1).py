from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from huggingface_hub import InferenceClient  # Use InferenceClient
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
# Fetch the API key from the environment variable
GOOGLE_API_KEY =  os.getenv("GOOGLE_API__KEY")

if not GOOGLE_API_KEY:
    raise ValueError("No API key found. Please set the GOOGLE_API_KEY environment variable.")

# Initialize the API with the fetched key
genai.configure(api_key=GOOGLE_API_KEY)


model= genai.GenerativeModel("gemini-1.5-flash")

# Load environment variables from .env file

# Get the Hugging Face API token from the environment
huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingfacehub_api_token:
    raise ValueError("Please set the HUGGINGFACEHUB_API_TOKEN in the .env file.")

# Initialize the embedding model for the knowledge base
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Create a knowledge base with FAISS
documents = [
    "The moon is Earth's only natural satellite.",
    "Love is a strong positive emotion of deep affection.",
    "Ernest Hemingway was an American novelist and short-story writer."
]

vectorstore = FAISS.from_texts(documents, embedding=embedding_model)

# # Initialize the Hugging Face Inference Client
# model_name = "facebook/blenderbot-400M-distill"  # Use a conversational model
# inference_client = InferenceClient(model=model_name, token=huggingfacehub_api_token)

# Function to retrieve relevant documents
def retrieve_documents(query, k=2):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)  # Use invoke instead of get_relevant_documents

# Function to generate a response using the Inference Client
def generate_response(query, context):
    prompt = f"You are a helpful AI assistant. Use the following context to answer the user's question:\n\nContext: {context}\n\nQuestion: {query}\nAnswer:, also make sure the answer is more than just the context and more creative"
    # print("Prompt sent to the model:", prompt)  # Debugging: Print the prompt
    response = model.generate_content(prompt)
    return response.text

# Function to interact with the RAG chatbot
def chat():
    print("RAG Chatbot is ready! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        # Retrieve relevant documents
        relevant_docs = retrieve_documents(user_input)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        # print("Retrieved context:", context)  # Debugging: Print the retrieved context
        # Generate a response using the Inference Client
        response = generate_response(user_input, context)
        print(f"Chatbot: {response}")

# Start the chat
if __name__ == "__main__":
    chat()




