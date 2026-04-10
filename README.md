# Zambian Road Traffic & Vehicle Rights AI Assistant

A specialized Retrieval-Augmented Generation (RAG) application that provides accurate answers about Zambian road traffic laws, vehicle regulations, and driver rights based on official transportation legal documents.

## Features

- **RAG Architecture**: Prevents AI hallucinations by forcing answers to be based on actual traffic law text
- **Source Citation**: Shows which traffic acts and regulations were used to generate answers
- **Self-Checking**: Verifies answer relevance before displaying to users
- **Traffic Law Focus**: Specialized in road traffic, vehicle regulations, and RSTA procedures
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Factual Accuracy**: Uses Groq's Llama 3.1 model for reliable legal reasoning

## Technical Stack

- **Language**: Python 3.12+
- **Framework**: LangChain for RAG pipeline
- **LLM**: Groq (Llama 3.1 8B Instant)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Frontend**: Streamlit
- **Document Processing**: PyPDF

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the ingestion script** (only once or when adding new documents):
   ```bash
   python ingest_data.py
   ```

5. **Start the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open your browser and navigate to `http://localhost:8501`
2. Enter your road traffic question about Zambian transportation laws
3. Click "Get Traffic Law Answer" to receive a factual response
4. Expand "Traffic Law Sources Used" to see the specific documents referenced

## Example Questions

- "What are the requirements for a driver's license?"
- "What constitutes dangerous driving under the Road Traffic Act?"
- "What are vehicle registration requirements in Zambia?"
- "What are the fines for traffic violations?"
- "How do I appeal a traffic ticket?"
- "What are pedestrian rights on roads?"
- "What are the speed limits on urban roads?"

## Project Structure

```
zambian-rights-ai/
|-- app.py              # Main Streamlit application
|-- ingest_data.py      # Document ingestion script
|-- test_rag.py         # RAG pipeline testing script
|-- clean_database.py   # Database cleaning script
|-- requirements.txt    # Python dependencies
|-- .env               # Environment variables (create this)
|-- laws/              # Directory for traffic law PDFs
|   |-- road_traffic_act.pdf
|   |-- (add more traffic law documents here)
|-- chromadb_storage/  # Vector database (created automatically)
```

## How It Works

### 1. Document Ingestion
- Loads traffic law PDF files from the `laws/` directory
- Splits documents into manageable chunks (1000 characters with 200 overlap)
- Converts text to numerical embeddings using HuggingFace
- Stores embeddings in ChromaDB for fast retrieval

### 2. Question Answering
- User asks a road traffic question
- System retrieves relevant traffic law chunks using similarity search
- Context is passed to the LLM with specific traffic law instructions
- LLM generates answer based ONLY on provided transportation legal text
- Self-checking mechanism verifies answer relevance

### 3. Safety Features
- **No Hallucinations**: AI cannot make up traffic laws - must use provided text
- **Source Transparency**: Shows exactly which traffic documents were referenced
- **Relevance Checking**: Verifies answers actually address the traffic question
- **Fallback Handling**: Gracefully handles missing traffic information

## Adding New Traffic Law Documents

1. Place new traffic law PDF files in the `laws/` directory
   - Road Traffic Regulations
   - RSTA Procedures
   - Vehicle Registration Laws
   - Highway Safety Regulations
2. Run the ingestion script again:
   ```bash
   python ingest_data.py
   ```
3. Restart the Streamlit app

## API Keys

You'll need a Groq API key for the LLM:
1. Sign up at [console.groq.com](https://console.groq.com)
2. Create an API key
3. Add it to your `.env` file

## Testing

Run the test script to verify the RAG pipeline:
```bash
python test_rag.py
```

This will test:
- Database connection
- Document retrieval
- LLM generation

## Troubleshooting

### Common Issues

1. **"Legal database not found"**: Run `python ingest_data.py` first
2. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **API errors**: Check your Groq API key in the `.env` file
4. **Empty responses**: Verify the legal documents contain relevant information

### Performance Tips

- The first query may be slower as embeddings load into memory
- Subsequent queries will be faster
- Consider using a GPU for faster embeddings if available

## Contributing

To add new legal documents:
1. Ensure PDFs are official government documents
2. Place in the `laws/` directory
3. Run ingestion script
4. Test with relevant questions

## License

This project is for educational and informational purposes. Always consult with qualified legal professionals for official legal advice.

## Disclaimer

This AI assistant provides information based on the provided legal documents and should not be considered a substitute for professional legal advice. Laws may change, and legal interpretations can vary.
