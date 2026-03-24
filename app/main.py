from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Ismail's Portfolio API is running"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Vi importerar dessa INUTI funktionen istället för längst upp
    # Detta sparar RAM-minne vid uppstart!
    from app.retriever import search_index
    from app.llm import generate_answer
    
    relevant_chunks = search_index(request.message)
    answer = generate_answer(request.message, relevant_chunks)
    
    return {"answer": answer}