# AI Investigation RAG Engine

## Project Description
Professional RAG-based Investigation Assistant designed to analyze documents, extract evidence, detect conflicts between reports, and provide accurate answers with strict source attribution.

## Architecture & Tech Stack
- **Frontend/UI:** Streamlit
- **Vector Database:** ChromaDB (Persistent Client with Auto-Seeding)
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **LLM:** Google Gemini API (`google-generativeai`)
- **Evaluation:** Custom automated evaluation script (`evaluate.py`)

## Setup & Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with `GEMINI_API_KEY`.
4. Run the app: `streamlit run app.py`
