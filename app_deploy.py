import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Zambian Road Traffic AI",
    layout="wide"
)

st.title("Zambian Road Traffic & Vehicle Rights AI Assistant")
st.markdown("*Ask questions about road traffic laws, vehicle regulations, and driver rights*")

# Check if API key is available
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key Required")
    st.warning("Please add GROQ_API_KEY to your Streamlit Cloud secrets")
    st.stop()

st.success("Ready for questions!")
st.write("This is a deployment-ready version.")

question = st.text_input("Ask your road traffic question:")
if question and st.button("Get Answer"):
    st.info("Full RAG functionality will be available once database is ready.")
    st.write(f"You asked: {question}")

st.markdown("---")
st.markdown("*Zambian Road Traffic AI Assistant*")
