#!/usr/bin/env python3
"""
Test script to verify the RAG pipeline functionality
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Constants
CHROMA_PATH = "chromadb_storage"

def test_rag_pipeline():
    """Test the complete RAG pipeline"""
    print(" Testing Zambian Road Traffic AI RAG Pipeline")
    print("=" * 50)
    
    # Test 1: Database initialization
    print("\n1. Testing Database Connection...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        print(" Database connected successfully!")
        
        # Check if we have documents
        collection = db._collection
        doc_count = collection.count()
        print(f" Found {doc_count} document chunks in database")
        
    except Exception as e:
        print(f" Database connection failed: {e}")
        return False
    
    # Test 2: Retrieval
    print("\n2. Testing Document Retrieval...")
    test_query = "What are the requirements for a driver's license?"
    
    try:
        results = db.similarity_search(test_query, k=3)
        print(f" Retrieved {len(results)} relevant documents")
        
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'Unknown')
            print(f" Document {i}: {source} (Page {page})")
            print(f" Preview: {doc.page_content[:100]}...")
            print()
            
    except Exception as e:
        print(f" Retrieval failed: {e}")
        return False
    
    # Test 3: LLM Generation (if API key is available)
    print("\n3. Testing LLM Generation...")
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        print(" GROQ_API_KEY not found in environment variables")
        print(" Skipping LLM test...")
        return True
    
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            groq_api_key=groq_api_key
        )
        
        # Create a simple test prompt
        prompt = ChatPromptTemplate.from_template("""
        You are a Zambian Road Traffic assistant. Based on the following context, answer the question.
        
        Context: {context}
        Question: {question}
        
        Provide a brief, factual answer about road traffic laws.
        """)
        
        # Use the first retrieved document as context
        context = results[0].page_content if results else "No context available"
        
        formatted_prompt = prompt.format(context=context, question=test_query)
        response = llm.invoke(formatted_prompt)
        
        print(" LLM Response:")
        print(response.content[:200] + "..." if len(response.content) > 200 else response.content)
        print(" LLM test successful!")
        
    except Exception as e:
        print(f" LLM test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print(" All Road Traffic RAG pipeline tests completed successfully!")
    return True

if __name__ == "__main__":
    test_rag_pipeline()
