from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag_chain import generate_answer

app = FastAPI(title="AWS S3 RAG Chatbot")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    answer = generate_answer(request.question)
    return {"answer": answer}
