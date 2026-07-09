import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

def get_embeddings():
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=os.environ.get("HF_TOKEN"),
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings
