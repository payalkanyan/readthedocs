from rag.datasetloader import load as ds_loader
from rag.preprocessing import preprocess_text
from rag.embeddings import get_embeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma


PERSIST_DIR = "vectorstore/chroma_db"

def build_index():
    all_text = ds_loader()
    chunks = preprocess_text(all_text)
    documents = [Document(page_content=chunk) for chunk in chunks]

    embeddings = get_embeddings()
    Chroma.from_documents(
        documents = documents, 
        embedding = embeddings,
        persist_directory = PERSIST_DIR
    ) 

    print("Chroma DB built successfully")

if __name__ == "__main__":
    build_index()
