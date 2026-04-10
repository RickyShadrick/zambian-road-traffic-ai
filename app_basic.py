import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Zambian Road Traffic AI",
    layout="wide"
)

st.title("Zambian Road Traffic AI Assistant")
st.markdown("*Ask questions about Zambian road traffic laws*")

# Check if API key is available
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key Required")
    st.warning("Please add GROQ_API_KEY to your Streamlit Cloud secrets")
    st.stop()

st.success("Ready for questions!")
st.write("This is a basic version for testing deployment.")

question = st.text_input("Ask your road traffic question:")
if question and st.button("Get Answer"):
    st.info("Basic version - no database connection yet.")
    st.write(f"You asked: {question}")
    
    # Test API key connection
    if api_key:
        st.success(f"API key found: {api_key[:10]}...")

st.markdown("---")
st.markdown("*Basic Zambian Road Traffic AI Assistant*")
