import os
from langchain_huggingface import HuggingFaceEndpointEmbeddings

os.environ["HF_TOKEN"] = "hf_dummy"
try:
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        task="feature-extraction",
        huggingfacehub_api_token=os.environ["HF_TOKEN"]
    )
    print("Successfully instantiated")
except Exception as e:
    print("Error:", e)
