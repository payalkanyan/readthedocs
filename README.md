Offline (build_index.py):
    load PDFs → preprocess → create embeddings → save FAISS index

Backend (server / chatbot):
    load FAISS index from disk → answer user queries



# AWS S3 RAG Chatbot

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot over AWS S3 documentation using **LangChain, FAISS, and Hugging Face models**.
PDFs are processed **offline**, and the backend serves fast, retrieval-based answers via a REST API.

---

## Architecture Overview

* **Offline step**:
  PDFs → text → chunks → embeddings → FAISS index (saved to disk)
* **Runtime backend**:
  Load FAISS once → retrieve relevant chunks → generate answer with LLM
* **No PDF loading at query time**

---

## Setup

### 1. Create virtual environment

```bash
python -m venv myenv
source myenv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure you have a valid Hugging Face token set in `app/config.py` or as an environment variable.

---

## Build the FAISS Index (One-time)

Run this **once** whenever documents change:

```bash
python -m rag.builtindex
```

This will:

* Load PDFs from `docs/aws_s3/`
* Split text into chunks
* Generate embeddings
* Save FAISS index to `vectorstore/faiss_index/`

---

## Run the Backend

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## Test the API

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

Use **POST /chat** with:

```json
{
  "question": "What is Amazon S3 Glacier?"
}
```

