import os
from langchain_ollama import OllamaEmbeddings

EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def get_embeddings():
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
