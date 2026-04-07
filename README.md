# Project Nexus - Limi AI Assessment Solution

This is a complete working solution for the Limi AI technical assessment.

It includes:
- FastAPI backend
- LangChain-based RAG pipeline
- PDF ingestion with ChromaDB
- Two-agent workflow: Researcher + Critic
- React + Tailwind frontend
- Streaming chat response with SSE
- Mermaid architecture design for scale

## Folder structure

```bash
limi_ai_assessment/
├── backend/
│   ├── app/
│   ├── data/
│   ├── ingest.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── tailwind.config.js
├── DESIGN.md
└── README.md
```

## Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your Hugging Face token in `.env`:

```env
HUGGINGFACEHUB_ACCESS_TOKEN=your_token_here
HF_REPO_ID=mistralai/Mistral-7B-Instruct-v0.3
```

## Put PDFs in the data folder

Place any PDF inside:

```bash
backend/data/
```

A dummy sample PDF is already included.

## Run ingestion

```bash
python ingest.py
```

## Start backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```bash
http://127.0.0.1:5173
```

## API endpoints

### 1. Check app
```bash
GET /
```

### 2. Upload PDF
```bash
POST /upload
```

### 3. Ingest PDFs
```bash
POST /ingest
```

### 4. Normal chat
```bash
POST /chat
```
Body:
```json
{
  "question": "What is the refund policy?"
}
```

### 5. Streaming chat
```bash
GET /chat/stream?question=What+is+the+refund+policy
```

## Notes about the agent workflow

The backend uses a simple event-driven workflow:

1. `question.received`
2. `research.completed`
3. `critic.completed`

- The **Researcher agent** retrieves chunks from the vector store.
- The **Critic agent** checks the context and writes a grounded answer.

## Why this solution matches the assessment

### 1. RAG pipeline
- PDF loading
- chunking
- embeddings
- Chroma vector database
- question answering with context

### 2. Multi-agent system
- Researcher agent
- Critic agent
- structured events

### 3. Full-stack interface
- React frontend
- Tailwind styling
- SSE streaming
- citations shown in UI

### 4. Architecture and scalability
- `DESIGN.md` includes Mermaid diagram
- rate limiting, caching, scaling, model latency handling included

## Suggested GitHub repo name

```bash
limi-ai-project-nexus
```

## Final tip before submission

Record a short demo video or screenshots showing:
- PDF upload
- ingestion
- streamed answer
- citations panel
- design file

That will make your submission stronger.
