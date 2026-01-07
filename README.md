# AWS S3 RAG


## Setup

1. **Create `.env` file**

Create a `.env` file in the root directory with the following variables:

```env
HF_TOKEN = hf_token
```

2. **Install Python dependencies (optional for local development)**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running with Docker

The backend is fully containerized. You can run it with:

```bash
sudo docker run -d \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/vectorstore/chroma_db:/app/vectorstore/chroma_db \
  aws-s3-rag
```

* `-p 8000:8000` exposes the backend on port 8000.
* `--env-file .env` loads environment variables inside the container.
* `-v $(pwd)/vectorstore/chroma_db:/app/vectorstore/chroma_db` mounts the local vector store into the container.
* `-d` runs the container in detached mode.

**Verify the container is running:**

```bash
sudo docker ps
```

**Check logs:**

```bash
sudo docker logs -f <container_id>
```

