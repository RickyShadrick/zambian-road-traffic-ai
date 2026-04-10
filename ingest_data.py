import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Setup - Tell the app where the laws are
LAWS_DIR = "laws"
CHROMA_PATH = "chromadb_storage"

def ingest_laws():
    # 2. Load PDFs
    documents = []
    for file in os.listdir(LAWS_DIR):
        if file.endswith(".pdf"):
            print(f"Reading {file}...")
            loader = PyPDFLoader(os.path.join(LAWS_DIR, file))
            documents.extend(loader.load())

    # 3. Chunking - Breaking long laws into smaller pieces
    # We use 1000 characters with 200 overlap so no law is cut in half
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks of legal text.")

    # 4. Embeddings - This turns text into numbers the AI understands
    # We use a free model from HuggingFace that runs on your computer
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. Store in ChromaDB
    print("Saving to database...")
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=CHROMA_PATH
    )
    print("Success! Your Zambian Legal Database is ready.")

if __name__ == "__main__":
    ingest_laws()
