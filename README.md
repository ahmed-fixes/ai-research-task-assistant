# AI Research & Task Assistant

An AI-powered assistant built with **FastAPI, LangGraph, and Groq** that routes user requests to the appropriate workflow: direct LLM answers, retrieval-augmented generation (RAG) over uploaded documents, or tool execution.

> This repository currently focuses on the backend. A dedicated frontend may be added later.

## Features

- **Intelligent request routing:** LangGraph coordinates the workflow based on the user's request.
- **Direct answers:** Uses a Groq-hosted LLM for general questions.
- **Document Q&A (RAG):** Embeds document chunks, searches relevant content with FAISS, and uses retrieved context to answer questions.
- **Source information:** Can return source metadata associated with retrieved document chunks.
- **Calculator tool:** Evaluates supported mathematical expressions through a dedicated tool.
- **Weather tool:** Retrieves weather information for a specified city through the configured weather service.
- **Conversation sessions:** Maintains session-based message history for continuing conversations.
- **Document management:** Supports adding/uploading, listing, and deleting documents through the implemented backend endpoints.
- **Validation and error handling:** Uses Pydantic schemas and structured tool execution.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | REST API |
| LangGraph | Agent workflow and routing |
| Groq API | LLM inference |
| Qwen model | Configured language model |
| Sentence Transformers | Text embeddings |
| `all-MiniLM-L6-v2` | Embedding model |
| FAISS | Vector similarity search |
| SQLAlchemy | Database ORM |
| SQLite | Document metadata storage |
| Pydantic | Request and data validation |
| OpenWeather API | Weather data, if configured |

## How It Works

```text
User Request
     |
     v
FastAPI Endpoint
     |
     v
LangGraph Agent
     |
     +---- Direct Question ----> LLM ----> Answer
     |
     +---- Document Question --> Embedding --> FAISS Search
     |                                      |
     |                                      v
     |                              Retrieved Context
     |                                      |
     |                                      v
     |                                     LLM
     |
     +---- Tool Request --------> Tool Selection
                                      |
                                      +---- Calculator
                                      |
                                      +---- Weather
     |
     v
Response returned to the client
```

The frontend sends requests to the API. The backend selects the appropriate workflow and returns an answer with available metadata, such as actions, sources, session ID, or errors.

## Project Structure

The following is an illustrative structure. Check the actual repository before relying on individual filenames.

```text
ai-research-task-assistant/
├── app/
│   ├── agent/          # Agent nodes, routing, and graph
│   ├── routers/        # FastAPI endpoints
│   ├── services/       # LLM, embeddings, and document services
│   ├── tools/          # Calculator and weather tools
│   ├── vectorstore/    # FAISS vector store
│   ├── storage/        # Session/checkpoint storage
│   ├── models.py       # Database models
│   ├── schemas.py      # Pydantic schemas
│   └── main.py         # FastAPI application
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- A Python version compatible with the dependencies in `requirements.txt`
- A Groq API key
- An OpenWeather API key if the weather tool uses OpenWeather
- Internet access for external API calls and any model downloads not already cached locally

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-research-task-assistant.git
cd ai-research-task-assistant
```

Replace `YOUR-USERNAME` with the GitHub account that owns the repository.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file based on `.env.example`, if the project uses one. Add the variable names expected by the actual configuration code. For example:

```dotenv
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

These names are examples; confirm the exact names in the project's configuration and tool files. **Never commit `.env` or real API keys to GitHub.**

### 5. Run the API

If `app/main.py` defines the FastAPI application as `app`, run:

```powershell
uvicorn app.main:app --reload
```

Open the API documentation in your browser:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

If the application uses a different import path or port, follow the actual project configuration.

## API Capabilities

The project has included the following agent/session routes during development:

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/agent/run` | Submit a request to the agent |
| `POST` | `/agent/chat` | Chat endpoint |
| `GET` | `/sessions/{session_id}` | Retrieve session information |
| `DELETE` | `/sessions/{session_id}` | Delete a session |

Document-management endpoints are also part of the intended backend functionality for adding/uploading, listing, and deleting documents.

**Verify the current FastAPI router and request/response schemas** in `/docs` or the source code for exact payloads, HTTP methods, and document endpoint paths. This table describes routes used during development and should not replace the running API's actual schema.

## Example Use Cases

**General question**

> Explain the difference between supervised and unsupervised learning.

**Document question**

> According to the uploaded company policy, how many annual leave days are available?

**Calculator**

> Calculate 25 multiplied by 8.

**Weather**

> What is the weather in Lahore?

The available answer details depend on the LLM response, uploaded documents, configured API keys, and tool results.

## RAG Workflow

1. A supported document is added through the document API.
2. Its text is processed and divided into chunks.
3. The embedding model converts chunks into vectors.
4. FAISS stores the vectors with associated metadata.
5. A user's question is converted into an embedding.
6. FAISS retrieves relevant chunks.
7. The backend builds a context-based prompt and asks the LLM to answer.
8. Available source metadata is returned with the response.

If the uploaded documents do not contain enough relevant information, the answer should not be presented as verified. Display source metadata only when it is returned by the backend and relevant to the answer.

## Security Notes

- Never commit `.env`, API keys, tokens, or other credentials.
- Keep virtual environments, Python cache folders, and unnecessary generated files out of Git.
- Do not expose backend API keys in a future frontend.
- Validate user inputs and handle API failures safely.
- Review uploaded documents and local database/vector-store files before publishing them.
- Configure CORS for the intended frontend origin when frontend integration is added.

## Current Scope

The backend demonstrates an AI agent that can select between direct LLM answering, document retrieval, and tool execution. A professional web frontend can be added later and connected to the existing FastAPI endpoints.

## Future Improvements

- Add a responsive frontend for chat and document management.
- Add tests for routing, tools, RAG retrieval, and API endpoints.
- Improve observability and structured logging.
- Add support for additional document formats only after implementing and testing their ingestion pipelines.

## Author

**Muhammad Ahmed Amir**

- GitHub: [ahmed-fixes](https://github.com/ahmed-fixes)

---

*Update this README whenever API routes, environment variables, supported file formats, or implemented features change.*
