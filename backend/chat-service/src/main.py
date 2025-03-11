from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid

app = FastAPI(
    title="GenAI Chat Platform - Chat Service",
    description="Handles chat logic for the GenAI Chat Platform",
    version="0.1.0"
)

# In-memory storage for conversations
conversations: Dict[str, List[dict]] = {}

class ChatMessage(BaseModel):
    content: str
    role: str  # user or assistant
    timestamp: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    # Generate a conversation ID if not in context
    conversation_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    # Store the user message
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    conversations[conversation_id].append({
        "content": message.content,
        "role": "user",
        "timestamp": timestamp
    })
    
    # Generate response
    response_text = f"Echo: {message.content}"
    
    # Store the assistant's response
    conversations[conversation_id].append({
        "content": response_text,
        "role": "assistant",
        "timestamp": timestamp
    })
    
    return ChatResponse(
        message=response_text,
        conversation_id=conversation_id,
        timestamp=timestamp
    )

@app.get("/conversations/{conversation_id}", response_model=List[ChatMessage])
async def get_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return [ChatMessage(**msg) for msg in conversations[conversation_id]]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 