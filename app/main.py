from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# comment out these for a moment
# from app.retriever import search_index
# from app.llm import generate_answer

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
    return {"status": "ok", "message": "Backend is alive"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Enkelt svar utan AI för att testa porten
    return {"answer": f"Backend mottog: {request.message}. AI laddas fortfarande..."}