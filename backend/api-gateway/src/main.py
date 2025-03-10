# Import necessary libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # For handling cross-origin requests

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

# Define a simple health check endpoint
@app.get("/health")         # HTTP GET endpoint at /health
async def health_check():   # Async function for better performance
    return {
        "status": "healthy",
        "service": "api-gateway"
    }

# Run the application if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run on all network interfaces, port 8000 