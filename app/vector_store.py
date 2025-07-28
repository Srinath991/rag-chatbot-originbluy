# app/pinecone_store.py

import pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.embeddings.base import Embeddings
from langchain.schema.document import Document
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

def create_vector_store(
    docs: List[Document],
    embeddings: Embeddings,
    index_name: str=os.getenv("PINECONE_INDEX", "rag-index")
) -> Pinecone:
    """
    Create and upload a Pinecone index with embedded documents.
    Assumes index already exists in Pinecone dashboard.
    """
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)

    # Create and upload to Pinecone index
    vector_store = PineconeVectorStore(index=index,embedding=embeddings)
    vector_store.add_documents(docs)
    return vector_store

def load_vector_store(
    embeddings: Embeddings,
    index_name: str = os.getenv("PINECONE_INDEX")
) -> Pinecone:
    """
    Load an existing Pinecone index for retrieval.
    """
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)

    # Create and upload to Pinecone index
    vector_store = PineconeVectorStore(index=index,embedding=embeddings)
    return vector_store