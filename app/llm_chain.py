from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def get_rag_chain(retriever, llm=None):
    if llm is None:
        llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are answering as a {role}. Use the following context to answer the question. Cite sources."),
        ("human", "{context}\n\nQuestion: {question}")
    ])
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])
    def get_sources(docs):
        return list({d.metadata.get('source', '') for d in docs if d.metadata.get('source')})
    def rag_with_sources(inputs):
        docs = retriever.invoke(inputs["question"])
        context = format_docs(docs)
        role = inputs.get("role") or "user"
        answer = llm.invoke(prompt.invoke({"context": context, "question": inputs["question"], "role": role}))
        sources = get_sources(docs)
        return {"answer": answer.content if hasattr(answer, 'content') else str(answer), "sources": sources}
    return rag_with_sources 