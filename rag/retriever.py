from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings

VECTORSTORE_PATH = "vectorstore/faiss_index"

_embeddings = get_embeddings()
_vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    _embeddings,
    allow_dangerous_deserialization=True
)

def retrieve(k: int = 6):
    """
    Returns a LangChain retriever instance.
    """
    return _vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
