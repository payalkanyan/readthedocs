from rag.datasetloader import load as ds_loader
from rag.preprocessing import preprocess_text
from rag.embeddings import get_embeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


def build_index():
    all_text = ds_loader()
    chunks = preprocess_text(all_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    embeddings = get_embeddings()
    db = FAISS.from_documents(docs, embeddings) 
    db.save_local("vectorstore/faiss_index")

    print("FAISS index built")

if __name__ == "__main__":
    build_index()
