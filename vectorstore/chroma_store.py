from langchain_community.vectorstores import Chroma
from rag.embeddings import get_embeddings

PERSIST_DIR = "vectorstore/chroma_db"

def get_retriever():
    embeddings = get_embeddings()

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
