from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rag.rag_chain import generate_answer
import traceback

app = FastAPI(title="AWS S3 RAG Chatbot")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = traceback.format_exc()
    return JSONResponse(status_code=500, content={"detail": str(exc), "traceback": error_msg})

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
