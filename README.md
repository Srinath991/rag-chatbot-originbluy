# RAG-based Chatbot System

## Setup Instructions

1. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```sh
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY=...
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   # or, if using uv:
   uv pip install -r requirements.txt
   ```
3. Add your sample documents (PDF, DOCX, TXT) to the `docs/` folder.
4. Run the backend API:
   ```sh
   uvicorn main:app --reload
   ```

## Libraries Used
- FastAPI
- Uvicorn
- LangChain (with OpenAI)
- Chroma
- PyMuPDF
- PyPDF2
- python-docx
- python-dotenv

## Sample Queries
- "Summarize the key points from the employee handbook."
- "What is the leave policy?"

## Notes
- Embeddings and LLM responses use OpenAI APIs (API key required, see `.env.example`).
- Only basic retrieval and citation are implemented in the MVP.
- Add your documents to the `docs/` folder before running ingestion.
- Limitations: No role-based filters, feedback, or frontend in MVP. Additions welcome!
