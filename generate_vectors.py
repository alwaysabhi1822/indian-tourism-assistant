# generate_vectors.py
import os
import pickle
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Configuration ---
TEXT_FILE_PATH = "total_data.txt" # Your single text file
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "vectors.pkl"

# --- 1. Load your document ---
if not os.path.exists(TEXT_FILE_PATH):
    print(f"Error: The file '{TEXT_FILE_PATH}' was not found in the current directory.")
    print("Please make sure 'total_data.txt' is in the same folder where you run this script.")
    exit()

# *** IMPORTANT CHANGE HERE: Specify encoding='utf-8' ***
loader = TextLoader(TEXT_FILE_PATH, encoding='utf-8')
documents = loader.load()

if not documents:
    print(f"No content found in '{TEXT_FILE_PATH}'. Please ensure it contains text data.")
    exit()
else:
    print(f"Loaded {len(documents)} document from '{TEXT_FILE_PATH}'.")

# --- 2. Split documents into chunks ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")

# --- 3. Initialize embeddings model ---
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
print(f"Embeddings model '{EMBEDDING_MODEL_NAME}' loaded.")

# --- 4. Create and save the FAISS vector store ---
print("Creating FAISS vector store from chunks...")
vectors = FAISS.from_documents(chunks, embeddings)
print("FAISS vector store created.")

# --- 5. Save the vector store to a pickle file ---
try:
    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump(vectors, f)
    print(f"Vector store successfully saved to '{VECTOR_STORE_PATH}'")
except Exception as e:
    print(f"Error saving vector store: {e}")