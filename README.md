# RAG-based Chatbot System

## Setup Instructions
1. Clone the Repo:
   ```sh
   git clone https://github.com/Srinath991/rag-chatbot-originbluy
   cd rag-chatbot-originbluy
   ```
1. Copy `.env.example` to `.env` and add your API keys:
   ```sh
   cp .env.example .env
   # Edit .env and set 
   OPENAI_API_KEY=... 
   PINECONE_INDEX=.... 
   PINECONE_API_KEY=...
   ```
2. Install dependencies:
   ```sh
   uv sync
   ```
3. Add your sample documents (PDF, DOCX, TXT) to the `docs/` folder(or upload through UI).
4. Run the backend API:
   ```sh
   uv run uvicorn main:app --reload
   ```

## Libraries Used
- FastAPI
- LangChain (with OpenAI)
- Pinecone
- python-dotenv

## Sample Queries
- "Summarize the key points from the employee handbook."
- "What is the leave policy?"

## Notes
- Embeddings and LLM responses use OpenAI APIs (API keys required, see `.env.example`).
- Only basic retrieval and citation are implemented in the MVP.
- Add your documents to the `docs/` folder before running ingestion.
