from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="GenAI Chat Platform - Chat Service",
    description="Handles chat logic for the GenAI Chat Platform",
    version="0.1.0"
)

class ChatMessage(BaseModel):
    content: str
    role: str  # user or assistant

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    # Generate a response
    response_text = f"Echo: {message.content}"
    
    # Create the response in the expected format
    return ChatResponse(
        message=response_text,
        conversation_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 