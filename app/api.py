from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
import os
import shutil
import json
from contextlib import asynccontextmanager
from app.document_loader import load_and_split_documents
from app.embedding import get_embeddings
from app.vector_store import create_vector_store, load_vector_store
from app.llm_chain import get_rag_chain
from dotenv import load_dotenv
load_dotenv()

docs_dir = "docs"
chroma_dir = "chroma_db"
feedback_file = "feedback.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(chroma_dir, exist_ok=True)
    if not os.path.exists(feedback_file):
        with open(feedback_file, "w") as f:
            json.dump([], f)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/ingest/")
async def ingest_documents(files: List[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        dest = os.path.join(docs_dir, file.filename)
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(dest)
    docs = load_and_split_documents(file_paths)
    embeddings = get_embeddings()
    create_vector_store(docs, embeddings, chroma_dir)
    return {"status": "Documents ingested", "files": [os.path.basename(p) for p in file_paths]}

@app.post("/query/")
async def query_rag(query: str = Form(...), role: Optional[str] = Form(None)):
    embeddings = get_embeddings()
    vectordb = load_vector_store(embeddings, chroma_dir)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    rag_chain = get_rag_chain(retriever)
    result = rag_chain({"question": query, "role": role})
    answer = result["answer"]
    citations = [os.path.basename(src) for src in result["sources"] if src]
    return {"response": answer, "citations": citations}

@app.post("/feedback/")
async def submit_feedback(query: str = Form(...), response: str = Form(...), helpful: bool = Form(...), role: Optional[str] = Form(None)):
    feedback = {
        "query": query,
        "response": response,
        "helpful": helpful,
        "role": role
    }
    try:
        with open(feedback_file, "r+") as f:
            data = json.load(f)
            data.append(feedback)
            f.seek(0)
            json.dump(data, f, indent=2)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    return {"status": "success", "feedback": feedback} 