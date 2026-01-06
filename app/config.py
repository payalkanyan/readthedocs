import os
from dotenv import load_dotenv

load_dotenv()  

HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise RuntimeError("HF_TOKEN environment variable not set")
