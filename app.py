import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Constants
CHROMA_PATH = "chromadb_storage"

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are a Zambian Road Traffic and Vehicle Rights Assistant. Answer questions ONLY using the provided legal context from Zambian road traffic laws, RSTA regulations, and transportation legislation.

Rules:
1. Base your answers strictly on the provided road traffic and vehicle legal text
2. If the traffic laws don't mention the topic, clearly state "The provided road traffic documents do not contain information about this topic"
3. Always cite the specific traffic act, section, or regulation when possible
4. Do not make up or infer information beyond what's in the transportation text
5. Provide clear, practical explanations of road traffic rights and vehicle regulations
6. If multiple traffic laws apply, mention all relevant ones
7. Focus specifically on: driver rights, vehicle regulations, RSTA procedures, road safety, and transportation compliance

Context from Zambian Road Traffic Laws:
{context}

Question: {question}"""

def setup_database():
    """Initialize and return the Chroma database"""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        return db
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return None

def get_relevant_context(db, query, k=5):
    """Retrieve relevant legal context based on user query"""
    try:
        # Search for relevant documents
        results = db.similarity_search(query, k=k)
        
        # Format the context
        context_parts = []
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'Unknown')
            context_parts.append(f"Document {i} (Source: {source}, Page: {page}):\n{doc.page_content}")
        
        return "\n\n".join(context_parts)
    except Exception as e:
        st.error(f"Error retrieving context: {e}")
        return ""

def check_answer_relevance(question, context, answer):
    """Self-check mechanism to verify answer relevance"""
    try:
        # Simple relevance check - does the answer reference the context?
        if not answer or len(answer.strip()) < 50:
            return False, "Answer is too short or empty"
        
        # Check if answer mentions traffic law sources
        traffic_keywords = ["traffic", "road", "vehicle", "driver", "license", "rsta", "act", "section", "law", "legal", "according to", "states that", "regulation", "fine", "speed", "driving"]
        has_legal_reference = any(keyword.lower() in answer.lower() for keyword in traffic_keywords)
        
        if not has_legal_reference and len(context) > 100:
            return False, "Answer doesn't reference legal sources"
        
        return True, "Answer appears relevant"
    except Exception as e:
        return False, f"Error in relevance check: {e}"

def generate_answer(question, context):
    """Generate answer using Groq LLM"""
    try:
        # Initialize the LLM
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,  # Low temperature for factual answers
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        
        # Format the prompt with context and question
        formatted_prompt = prompt.format(context=context, question=question)
        
        # Generate response
        response = llm.invoke(formatted_prompt)
        
        return response.content
    except Exception as e:
        return f"Error generating answer: {e}"

def main():
    st.set_page_config(
        page_title="Zambian Road Traffic AI Assistant",
        page_icon="🚗",
        layout="wide"
    )
    
    # Header
    st.title("🚗 Zambian Road Traffic & Vehicle Rights AI Assistant")
    st.markdown("*Ask questions about road traffic laws, vehicle regulations, RSTA procedures, and driver rights based on official Zambian transportation documents*")
    
    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.info("""
        This AI assistant provides answers based on:
        - Road Traffic Act
        - RSTA Regulations
        - Vehicle Registration Laws
        - Driver License Requirements
        
        All answers are sourced from official transportation legal documents.
        """)
        
        st.header("Features")
        st.success("""
        - RAG Architecture
        - Source Citation
        - Self-Checking
        - Traffic Law Focus
        - Vehicle Rights Protection
        """)
    
    # Check if database exists
    if not os.path.exists(CHROMA_PATH):
        st.warning(" Legal database not found! Please run the ingestion script first.")
        st.code("python ingest_data.py")
        return
    
    # Initialize database
    db = setup_database()
    if not db:
        st.error("Failed to initialize database. Please check your setup.")
        return
    
    # Main interface
    st.header("Ask Your Road Traffic Question")
    
    # Example questions
    with st.expander("📋 Example Road Traffic Questions"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("🎗️ What are the requirements for a driver's license?")
            st.write("⚠️ What constitutes dangerous driving?")
            st.write("🚗 What are vehicle registration requirements?")
        with col2:
            st.write("💳 What are the fines for traffic violations?")
            st.write("🔷 How do I appeal a traffic ticket?")
            st.write("🚶 What are pedestrian rights on roads?")
    
    # Question input
    question = st.text_input(
        "Enter your road traffic question:",
        placeholder="e.g., What are the speed limits on urban roads?",
        key="question_input"
    )
    
    # Search and answer button
    if st.button("🚗 Get Traffic Law Answer", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
            return
        
        with st.spinner("Searching traffic laws and generating answer..."):
            # Step 1: Retrieve relevant context
            context = get_relevant_context(db, question)
            
            if not context:
                st.error("No relevant traffic law information found for your question.")
                return
            
            # Step 2: Generate answer
            answer = generate_answer(question, context)
            
            # Step 3: Self-check relevance
            is_relevant, check_message = check_answer_relevance(question, context, answer)
            
            # Display results
            st.subheader("📜 Traffic Law Answer")
            st.write(answer)
            
            # Show relevance check status
            if is_relevant:
                st.success(" Answer relevance: Verified")
            else:
                st.warning(f" Answer relevance: {check_message}")
            
            # Show context used
            with st.expander("📄 Traffic Law Sources Used"):
                st.text_area("Context", context, height=300, disabled=True)
    
    # Footer
    st.markdown("---")
    st.markdown("*Powered by RAG architecture - Specialized in Zambian Road Traffic Law*")

if __name__ == "__main__":
    main()