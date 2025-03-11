from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid
import logging
from logging.config import dictConfig

# Configure logging
log_config = {
    # Version of the logging configuration format
    "version": 1,
    
    # Don't turn off existing loggers when applying this configuration
    "disable_existing_loggers": False,
    
    # Define how log messages should be formatted
    "formatters": {
        "default": {
            # Log message format:
            # Example: "2024-03-11 12:30:45 - chat-service - INFO - Message received"
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            # Date format in the logs
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    
    # Define where logs should be sent
    "handlers": {
        "console": {
            # StreamHandler sends logs to console/terminal
            "class": "logging.StreamHandler",
            # Use the "default" formatter we defined above
            "formatter": "default",
            # Send to standard output (your terminal)
            "stream": "ext://sys.stdout",
        },
    },
    
    # Root logger configuration
    "root": {
        # Log level: DEBUG < INFO < WARNING < ERROR < CRITICAL
        "level": "INFO",
        # Use the "console" handler we defined above
        "handlers": ["console"]
    },
}

dictConfig(log_config)
logger = logging.getLogger("chat-service")

app = FastAPI(
    title="GenAI Chat Platform - Chat Service",
    description="Handles chat logic for the GenAI Chat Platform",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    try:
        logger.info(f"Received chat message: {message.content}")
        
        # Generate a conversation ID if not in context
        conversation_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Store the user message
        if conversation_id not in conversations:
            conversations[conversation_id] = []
            logger.info(f"Created new conversation with ID: {conversation_id}")
        
        conversations[conversation_id].append({
            "content": message.content,
            "role": "user",
            "timestamp": timestamp
        })
        
        # Generate response
        response_text = f"Echo: {message.content}"
        logger.info(f"Generated response: {response_text}")
        
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
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/conversations/{conversation_id}", response_model=List[ChatMessage])
async def get_conversation(conversation_id: str):
    try:
        logger.info(f"Fetching conversation: {conversation_id}")
        if conversation_id not in conversations:
            logger.warning(f"Conversation not found: {conversation_id}")
            raise HTTPException(status_code=404, detail="Conversation not found")
        return [ChatMessage(**msg) for msg in conversations[conversation_id]]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "chat-service",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Chat Service...")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 