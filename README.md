# AWS S3 RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using **FastAPI**, **ChromaDB**, and **Streamlit**, with Dockerized backend and frontend.
The system retrieves relevant context and generates answers using embeddings and LLMs.

---

* Frontend: Streamlit UI
* Backend: FastAPI (`/chat` endpoint)
* Vector store: Chroma (persistent volume)
* Deployment-ready using Docker

---


## Project Structure

```
readthedocs/
├── app/
├── rag/
├── vectorstore/
├── Dockerfile
├── requirements.txt
├── .env
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

---

## Running with Docker (Recommended)

### 1️⃣ Create Docker network

```bash
docker network create rag-network
```

---

### 2️⃣ Run Backend Container

From project root:

```bash
docker run -d \
  --name rag-backend \
  --network rag-network \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/vectorstore/chroma_db:/app/vectorstore/chroma_db \
  aws-s3-rag
```

Backend will be available at:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

---

### 3️⃣ Run Frontend Container

```bash
docker run -d \
  --name rag-frontend \
  --network rag-network \
  -p 8501:8501 \
  aws-s3-rag-frontend
```

Frontend UI:

```
http://localhost:8501
```

---

## Important Configuration

### Backend URL (Frontend)

Frontend reads backend URL from environment variable:

```python
BACKEND_URL = os.getenv("BACKEND_URL")
```

In Docker (local):

```
http://rag-backend:8000
```

---

## Stopping Containers

```bash
docker stop rag-backend rag-frontend
docker rm rag-backend rag-frontend
```

Docker images remain intact.

---
