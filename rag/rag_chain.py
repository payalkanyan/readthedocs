from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from vectorstore.chroma_store import get_retriever
from rag.prompt import get_prompt
from app.config import HF_TOKEN


prompt = get_prompt()
retriever = get_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_llm():
    hf_llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",
        huggingfacehub_api_token=HF_TOKEN,
        task="text-generation",
        max_new_tokens=300,
        temperature=0.1,
        top_p=0.9,
    )
    return ChatHuggingFace(llm=hf_llm)


def generate_answer(question: str) -> str:
    chat_llm = get_llm()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | chat_llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)