from langchain_community.vectorstores import Chroma

def create_vector_store(docs, embeddings, persist_directory):
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return vectordb

def load_vector_store(embeddings, persist_directory):
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings) 