import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents(doc_paths, chunk_size=1000, chunk_overlap=200):
    docs = []
    for path in doc_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".docx":
            loader = Docx2txtLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        else:
            continue
        docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs) 