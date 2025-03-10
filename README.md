# Multi-Modal GenAI Chatbot

A scalable, production-ready GenAI chatbot system that can handle large amounts of traffic.

## Project Structure

```
multi-modal-chatbot/
├── frontend/           # Next.js frontend application
├── backend/           # Backend microservices
│   ├── api-gateway/   # API Gateway service
│   ├── auth-service/  # Authentication service
│   ├── chat-service/  # Chat processing service
│   └── llm-service/   # LLM integration service
├── infrastructure/    # Infrastructure configurations
│   ├── docker/       # Docker configurations
│   └── kubernetes/   # Kubernetes configurations
└── docs/            # Project documentation
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- Docker Desktop
- Git

## Getting Started

1. Clone the repository
2. Install dependencies for each service
3. Set up environment variables
4. Run services using Docker Compose

## Development

Each service has its own README with specific setup instructions.

## License

MIT 