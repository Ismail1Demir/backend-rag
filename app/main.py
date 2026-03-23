from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.retriever import search_index
from app.llm import generate_answer

app = FastAPI()

# Tillåt frontend att anropa backenden
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
    # 1. Hämta relevant data från FAISS
    relevant_chunks = search_index(request.message)
    
    # 2. Skapa svar med LLM
    answer = generate_answer(request.message, relevant_chunks)
    
    # 3. Returnera svar
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)