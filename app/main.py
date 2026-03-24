from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# KOMMENTERA UT DESSA SÅ LÄNGE!
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

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Dummy-svar som inte kräver något RAM-minne!
    return {"answer": f"Wooohoo! 🎉 Backend mottog ditt meddelande: '{request.message}'. Vercel pratar med Render!"}