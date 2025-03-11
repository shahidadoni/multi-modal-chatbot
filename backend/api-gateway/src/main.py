# Import necessary libraries
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # For handling cross-origin requests
from pydantic import BaseModel
from typing import Optional, List
import httpx

# Create FastAPI application instance with metadata
app = FastAPI(
    title="GenAI Chat Platform - API Gateway",    # Name shown in API docs
    description="API Gateway for the GenAI Chat Platform",  # Description in API docs
    version="0.1.0"    # API version
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allows requests from any origin (not secure for production)
    allow_credentials=True,  # Allows cookies in cross-origin requests
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

# Data models
class ChatMessage(BaseModel):
    content: str
    role: str = "user"  # user or assistant
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    content: str
    role: str = "user"  # Default role

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: str

# Define a simple health check endpoint
@app.get("/health")         # HTTP GET endpoint at /health
async def health_check():   # Async function for better performance
    return {
        "status": "healthy",
        "service": "api-gateway"
    }

# Chat endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8001/chat", json=request.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Chat Service Error")
        return response.json()

@app.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessage])
async def get_conversation_messages(conversation_id: str):
    # TODO: Fetch from chat service
    return [
        ChatMessage(
            content="Hello!",
            role="user",
            timestamp="2024-03-11T00:00:00Z"
        ),
        ChatMessage(
            content="Hi there!",
            role="assistant",
            timestamp="2024-03-11T00:00:01Z"
        )
    ]

# Run the application if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Run on all network interfaces, port 8000 