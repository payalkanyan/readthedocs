from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag_chain import generate_answer

app = FastAPI(title="AWS S3 RAG Chatbot")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend is running!"}

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AWS S3 RAG API. The server is live!"}

@app.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    answer = generate_answer(request.question)
    return {"answer": answer}
