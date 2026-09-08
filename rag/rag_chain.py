import os
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from vectorstore.chroma_store import get_retriever
from rag.prompt import get_prompt

LLM_MODEL = "qwen2.5:1.5b"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

prompt = get_prompt()
retriever = get_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_llm():
    return ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.1, num_predict=300)


def generate_answer(question: str) -> str:
    chat_llm = get_llm()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | chat_llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)
